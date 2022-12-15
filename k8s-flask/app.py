from flask import Flask,render_template,request,jsonify
from celeryconfig import celery_app
from celery import Celery 
from celery.result import AsyncResult  
import celery.states as states
from textblob import TextBlob


app = Flask(__name__)

def search_recent_tweets(query, limit=15):
    q = "{}".format(query)
    r = celery_app.send_task("tasks.search", kwargs={"query":q, "limit":limit})
    return r.id

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search",methods=["POST"])
def search():
    search_tweet = request.form.get("search_query")
    t = []
    id=str(search_recent_tweets(str(search_tweet))) 
    res = celery_app.AsyncResult(id)
    tweets = list(res.get())
    # api.search(search_tweet, tweet_mode='extended')
    for tweet in tweets:
        polarity = TextBlob(tweet["text"]).sentiment.polarity
        subjectivity = TextBlob(tweet["text"]).sentiment.subjectivity
        t.append([tweet["text"],polarity,subjectivity])
        # t.append(tweet.full_text)

    return jsonify({"success":True,"tweets":t})

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
