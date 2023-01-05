from flask import Flask,render_template,request,jsonify, current_app
from celeryconfig import celery_hash, celery_loc

app = Flask(__name__)

def search_recent_tweets_hashtag(query, limit):
    q = "{}".format(query)
    r = celery_hash.send_task("hashtag_module.tasks.search", kwargs={"query":q, "limit":limit}, queue='hash_queue')
    return r.id

def search_recent_tweets_loc(query, limit):
    q = "{}".format(query)
    r = celery_loc.send_task("loc_module.tasks.search", kwargs={"query":q, "limit":limit}, queue='loc_queue')
    return r.id

def get_result(celery_app, return_id):
    res = celery_app.AsyncResult(return_id)
    tweets = list(res.get())
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
    search_prefer = request.form.get("search_prefer")

    if str(search_prefer).lower() ==  "city":
        id=str(search_recent_tweets_loc(str(search_tweet), int(search_number))) 
        all_tweets = get_result(celery_loc, id)
        tweets = all_tweets[0:-1]
        gen_wordcloud(str(all_tweets[-1]))
    else:
        id=str(search_recent_tweets_hashtag(str(search_tweet), int(search_number))) 
        all_tweets = get_result(celery_hash, id)
        tweets = all_tweets[0:-1]
        gen_wordcloud(str(all_tweets[-1]))
    return jsonify({"success":True,"tweets":tweets})

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")

