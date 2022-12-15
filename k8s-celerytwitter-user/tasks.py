from celeryconfig import celery_app
import celeryconfig
import tweepy


'''
The purpose of this script is to build upon the twitter_streamer.py script --
by importing its TwitterStreamer class and loading the collected, streamed tweets
into a MongoDB database.
'''

client = tweepy.Client(bearer_token=celeryconfig.BEARER_TOKEN)

def get_tweet_dict(tweet):

    '''Function that extracts relevant information from the tweet
       (using the 3 user-defined functions from above) and structures the
       data into a dictionary -- in preparation for loading into MongoDB.
    '''
    text = tweet['text']

    tweet = {'id': tweet['id'],
             'edit_history_tweet_ids': tweet['edit_history_tweet_ids'],
             'text': text,
             }
    return tweet

@celery_app.task
def insert_data(msg):
    return msg

@celery_app.task
def search(query, limit=10):
    tweets = client.search_recent_tweets(query=query, max_results=100)
    all_tweets = []
    count = 0
    for tweet in tweets.data:
        if "RT" not in tweet.text:
            t = get_tweet_dict(tweet.data)
            insert_data.delay(t)
            count += 1
            all_tweets.append(t)
            if count == limit:
                break
    return all_tweets




