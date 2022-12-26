from flask import Flask,render_template,request,jsonify, current_app
from celeryconfig import celery_hash, celery_loc
from celery import Celery 
from celery.result import AsyncResult  
import celery.states as states
from textblob import TextBlob
import time


app = Flask(__name__)

def search_recent_tweets_hashtag(query, limit):
    q = "{}".format(query)
    r = celery_hash.send_task("hashtag_module.tasks.search", kwargs={"query":q, "limit":limit})
    return r.id

def search_recent_tweets_loc(query, limit):
    q = "{}".format(query)
    r = celery_loc.send_task("loc_module.tasks.search", kwargs={"query":q, "limit":limit})
    return r.id

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search",methods=["POST"])
def search():
    search_tweet = request.form.get("search_query")
    search_number = request.form.get("search_number")
    search_prefer = request.form.get("search_prefer")
    t = []
    if str(search_prefer).lower ==  "city":
        id=str(search_recent_tweets_loc(str(search_tweet), int(search_number))) 
        res = celery_loc.AsyncResult(id)
        tweets = list(res.get())
        for tweet in tweets:
            polarity = TextBlob(tweet["text"]).sentiment.polarity
            subjectivity = TextBlob(tweet["text"]).sentiment.subjectivity
            t.append([tweet["text"],polarity,subjectivity])

        return jsonify({"success":True,"tweets":t})
    else:
        id=str(search_recent_tweets_hashtag(str(search_tweet), int(search_number))) 
        res = celery_hash.AsyncResult(id)
        tweets = list(res.get())
        for tweet in tweets:
            polarity = TextBlob(tweet["text"]).sentiment.polarity
            subjectivity = TextBlob(tweet["text"]).sentiment.subjectivity
            t.append([tweet["text"],polarity,subjectivity])

        return jsonify({"success":True,"tweets":t})

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
