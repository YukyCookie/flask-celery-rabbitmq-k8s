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

    pos_tweets = []
    neg_tweets = []
    opi_tweets = []
    fac_tweets = []
    text_lst = []
    
    text = ""
    pos_text = ""
    neg_text = ""
    opi_text = ""
    fac_text = ""
    
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        if polarity > 0 :
            pos_text = pos_text + " " + t["text"]
            pos_tweets.append([t["text"],polarity,subjectivity])
        elif polarity < 0:
            neg_text = neg_text + " " + t["text"]
            neg_tweets.append([t["text"],polarity,subjectivity])
        
        if subjectivity >= 0.5:
            opi_text = opi_text + " " + t["text"]
            opi_tweets.append([t["text"],polarity,subjectivity])
        elif subjectivity < 0.5:
            fac_text = fac_text + " " + t["text"]
            fac_tweets.append([t["text"],polarity,subjectivity])

        text = text + " " + t["text"]
        text_lst.append(t["text"])
        insert_data.delay(t)
        # all_tweets.append([t["text"],polarity,subjectivity])
    # wc_svg_all = cre_wordcloud(text)
    wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    wc_svg = wc.to_svg(embed_font=True)

    neu_len = limit-len(pos_tweets)-len(neg_tweets)
    all_tweets = {
        "pos_tweets": pos_tweets, 
        "pos_len": len(pos_tweets),
        "pos_text": pos_text,
        "neg_tweets": neg_tweets,
        "neg_len": len(neg_tweets),
        "neg_text": neg_text,
        "neu_len": neu_len,
        "opi_tweets": opi_tweets,
        "opi_len": len(opi_tweets),
        "opi_text": opi_text,
        "fac_tweets": fac_tweets,
        "fac_len": len(fac_tweets),
        "fac_text": fac_text,
        "text_list": text_lst,
        "wordcloud": """{}""".format(wc_svg),
        }
    
    # all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# search positive
@celery_app.task(queue='loc_senti')
def search_pos(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(100000)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if polarity > 0:
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
            if count == limit:
                break
    
    wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# search negative
@celery_app.task(queue='loc_senti')
def search_neg(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(100000)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if polarity < 0:    
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
            if count == limit:
                break
    
    wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets


# search opinion
@celery_app.task(queue='loc_senti')
def search_opi(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(100000)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if subjectivity >= 0.5: 
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
            if count == limit:
                break
    
    wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# search factual
@celery_app.task(queue='loc_senti')
def search_fac(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(100000)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if subjectivity < 0.5:
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
            if count == limit:
                break
    
    wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# select pos from all
@celery_app.task(queue='loc_senti')
def select_pos(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if polarity > 0:
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
    if count > 0: 
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    else:
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate("nothing")
    
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# select neg from all
@celery_app.task(queue='loc_senti')
def select_neg(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if polarity < 0:
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
    if count > 0: 
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    else:
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate("nothing")
    
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# select opi from all
@celery_app.task(queue='loc_senti')
def select_opi(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if subjectivity >= 0.5:
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
    if count > 0: 
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    else:
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate("nothing")
    
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

# select fac from all
@celery_app.task(queue='loc_senti')
def select_fac(query, limit):
    STOPWORDS.update(['https', query, 't', 'co', 'will', 'amp'])
    tweets = tweepy.Paginator(client.search_recent_tweets, query="entity:{} -is:retweet lang:en".format(query), max_results=100).flatten(limit)
    all_tweets = []
    text = ""
    count = 0
    for tweet in tweets:
        t = dict(tweet)
        polarity = TextBlob(t["text"]).sentiment.polarity
        subjectivity = TextBlob(t["text"]).sentiment.subjectivity
        
        if subjectivity < 0.5:
            count += 1
            text = text + " " + t["text"]
            all_tweets.append([t["text"],polarity,subjectivity])
    if count > 0: 
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate(text)
    else:
        wc = WordCloud(background_color="white", repeat=False ,stopwords=STOPWORDS, height=400, max_words=3000, width=1000, min_font_size=10, min_word_length=3).generate("nothing")
    
    wc_svg = wc.to_svg(embed_font=True)
    all_tweets.append("""{}""".format(wc_svg))
    return all_tweets

