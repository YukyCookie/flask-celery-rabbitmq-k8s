from flask import Flask,render_template,request,jsonify, current_app
from celeryconfig import celery_hash, celery_loc

app = Flask(__name__)


# search all the tweets with specific hashatg
def search_hashtag_all(query, limit):
    q = "{}".format(query)
    r = celery_hash.send_task("hashtag_module.tasks.search", kwargs={"query":q, "limit":limit}, queue='hash_queue')
    return r.id

def search_hashtag_senti(query, limit, task_name):
    q = "{}".format(query)
    r = celery_hash.send_task("hashtag_module.tasks.{}".format(task_name), kwargs={"query":q, "limit":limit}, queue='hash_senti')
    return r.id

# search all the tweets with specific location
def search_loc_all(query, limit):
    q = "{}".format(query)
    r = celery_loc.send_task("loc_module.tasks.search", kwargs={"query":q, "limit":limit}, queue='loc_queue')
    return r.id

def search_loc_senti(query, limit, task_name):
    q = "{}".format(query)
    r = celery_loc.send_task("loc_module.tasks.{}".format(task_name), kwargs={"query":q, "limit":limit}, queue='loc_senti')
    return r.id


def get_result_senti(celery_app, return_id):
    res = celery_app.AsyncResult(return_id)
    tweets = list(res.get())
    return tweets 

def get_result_all(celery_app, return_id):
    res = celery_app.AsyncResult(return_id)
    tweets = dict(res.get())
    return tweets 

def gen_wordcloud(wc_svg):
    f = open('static/img/wordcloud.svg', "w+")
    f.write(wc_svg)
    f.close()   



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search",methods=["POST"])
def search():
    search_tweet = request.form.get("search_query")
    search_number = request.form.get("search_number")
    select_search = request.form.get("select_search")
    select_result = request.form.get("select_result")
    
    if str(select_result).lower() == "all tweets":
        if str(select_search).lower() ==  "city":
            id=str(search_loc_all(str(search_tweet), int(search_number))) 
            all_tweets = get_result_all(celery_loc, id)

        elif str(select_search).lower() ==  "hashtag":
            id=str(search_hashtag_all(str(search_tweet), int(search_number))) 
            all_tweets = get_result_all(celery_hash, id)
        
        gen_wordcloud(str(all_tweets["wordcloud"]))

        return jsonify({
            "success":True, 
            "pos_len": all_tweets["pos_len"],
            "neg_len": all_tweets["neg_len"],
            "neu_len": all_tweets["neu_len"],
            "opi_len": all_tweets["opi_len"],
            "fac_len": all_tweets["fac_len"],
            "tweets": all_tweets["text_list"],
            "pos_tweets": all_tweets["pos_tweets"],
            "neg_tweets": all_tweets["neg_tweets"],
            "opi_tweets": all_tweets["opi_tweets"],
            "fac_tweets": all_tweets["fac_tweets"],
        })
    else:
        if str(select_search).lower() ==  "city":
            if str(select_result).lower() == "positive tweets":
                id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="search_pos"))

            elif str(select_result).lower() == "negative tweets": 
                id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="search_neg"))

            elif str(select_result).lower() == "opinion tweets": 
                id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="search_opi"))

            elif str(select_result).lower() == "factual tweets": 
                id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="search_fac"))
            
            all_tweets = get_result_senti(celery_loc, id)

        elif str(select_search).lower() ==  "hashtag":
            if str(select_result).lower() == "positive tweets":
                id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="search_pos"))

            elif str(select_result).lower() == "negative tweets": 
                id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="search_neg"))

            elif str(select_result).lower() == "opinion tweets": 
                id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="search_opi"))

            elif str(select_result).lower() == "factual tweets": 
                id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="search_fac"))
            
            all_tweets = get_result_senti(celery_hash, id)

        tweets = all_tweets[0:-1]
        gen_wordcloud(str(all_tweets[-1]))
        return jsonify({"success":True,"tweets":tweets})

@app.route("/search_pos",methods=["POST"])
def search_pos():
    search_tweet = request.form.get("search_query")
    search_number = request.form.get("search_number")
    select_search = request.form.get("select_search")
    select_result = request.form.get("select_result")

    if str(select_search).lower() ==  "city":
        id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="select_pos"))
        all_tweets = get_result_senti(celery_loc, id)

    elif str(select_search).lower() ==  "hashtag":
        id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="select_pos"))
        all_tweets = get_result_senti(celery_hash, id)
    
    tweets = all_tweets[0:-1]
    gen_wordcloud(str(all_tweets[-1]))

    return jsonify({"success":True,"tweets":tweets})

@app.route("/search_neg",methods=["POST"])
def search_neg():
    search_tweet = request.form.get("search_query")
    search_number = request.form.get("search_number")
    select_search = request.form.get("select_search")
    select_result = request.form.get("select_result")

    if str(select_search).lower() ==  "city":
        id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="select_neg"))
        all_tweets = get_result_senti(celery_loc, id)

    elif str(select_search).lower() ==  "hashtag":
        id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="select_neg"))
        all_tweets = get_result_senti(celery_hash, id)
    
    tweets = all_tweets[0:-1]
    gen_wordcloud(str(all_tweets[-1]))

    return jsonify({"success":True,"tweets":tweets})

@app.route("/search_opi",methods=["POST"])
def search_opi():
    search_tweet = request.form.get("search_query")
    search_number = request.form.get("search_number")
    select_search = request.form.get("select_search")
    select_result = request.form.get("select_result")

    if str(select_search).lower() ==  "city":
        id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="select_opi"))
        all_tweets = get_result_senti(celery_loc, id)

    elif str(select_search).lower() ==  "hashtag":
        id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="select_opi"))
        all_tweets = get_result_senti(celery_hash, id)
    
    tweets = all_tweets[0:-1]
    gen_wordcloud(str(all_tweets[-1]))

    return jsonify({"success":True,"tweets":tweets})

@app.route("/search_fac",methods=["POST"])
def search_fac():
    search_tweet = request.form.get("search_query")
    search_number = request.form.get("search_number")
    select_search = request.form.get("select_search")
    select_result = request.form.get("select_result")

    if str(select_search).lower() ==  "city":
        id=str(search_loc_senti(str(search_tweet), int(search_number), task_name="select_fac"))
        all_tweets = get_result_senti(celery_loc, id)

    elif str(select_search).lower() ==  "hashtag":
        id=str(search_hashtag_senti(str(search_tweet), int(search_number), task_name="select_fac"))
        all_tweets = get_result_senti(celery_hash, id)
    
    tweets = all_tweets[0:-1]
    gen_wordcloud(str(all_tweets[-1]))

    return jsonify({"success":True,"tweets":tweets})

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")

