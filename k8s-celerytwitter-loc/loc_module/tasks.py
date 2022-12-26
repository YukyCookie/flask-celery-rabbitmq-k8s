from loc_module.celery import celery_app
import loc_module.celery as celeryconfig
import tweepy

client = tweepy.Client(bearer_token=celeryconfig.BEARER_TOKEN)

@celery_app.task
def insert_data(msg):
    return msg

@celery_app.task
def search(query, limit):
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    for tweet in tweets:
        t = dict(tweet)
        insert_data.delay(t)
        all_tweets.append(t)
    return all_tweets
