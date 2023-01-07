from loc_module.celery import celery_app
import loc_module.celery as celeryconfig
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud,STOPWORDS

client = tweepy.Client(bearer_token=celeryconfig.BEARER_TOKEN)

@celery_app.task(queue='send_loc')
def insert_data(msg):
    return msg

@celery_app.task(queue='loc_queue')
def search(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    text = ""
    for tweet in tweets:
        t = dict(tweet)
        text = text + " " + t["text"]
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        insert_data.delay(t)
        all_tweets.append([t["text"],polarity,subjectivity])
    wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS,, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    
    return all_tweets
