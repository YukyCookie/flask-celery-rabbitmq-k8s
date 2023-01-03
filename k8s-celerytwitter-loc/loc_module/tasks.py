from loc_module.celery import celery_app
import loc_module.celery as celeryconfig
import tweepy
from textblob import TextBlob

client = tweepy.Client(bearer_token=celeryconfig.BEARER_TOKEN)

@celery_app.task(queue='send_loc')
def insert_data(msg):
    return msg

@celery_app.task(queue='loc_queue')
def search(query, limit):
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        insert_data.delay(t)
        all_tweets.append([t["text"],polarity,subjectivity])
    return all_tweets
