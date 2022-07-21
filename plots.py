import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def num_tweets(df):
    return df['date'].value_counts().sort_index()

def avg_polarity(df):
    return df.groupby('date')['polarity'].mean()


def tweets_per_day(df):
    pos = df[df["predicted-sentiment"]=="positive"]
    neg = df[df["predicted-sentiment"]=="negative"]
    neu = df[df["predicted-sentiment"]=="neutral"]

    # sentiment over time
    pos_pd = num_tweets(pos)
    neg_pd = num_tweets(neg)
    neu_pd = num_tweets(neu)
    avg_pd = num_tweets(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pos_pd.index, y=pos_pd,
        mode='lines',
        name='Positive'))
    fig.add_trace(go.Scatter(x=neu_pd.index, y=neu_pd,
        mode='lines',
        name='Neutral'))
    fig.add_trace(go.Scatter(x=neg_pd.index, y=neg_pd,
        mode='lines',
        name='Negative'))
    fig.add_trace(go.Scatter(x=avg_pd.index, y=avg_pd,
        mode='lines',
        name='Total'))
    fig.update_layout(
            title="Tweets per Day",
            xaxis_title="Day",
            yaxis_title="Num Tweets")
    return fig


def sentiment_over_time(df):
    pos = df[df["predicted-sentiment"]=="positive"]
    neg = df[df["predicted-sentiment"]=="negative"]
    neu = df[df["predicted-sentiment"]=="neutral"]

    # sentiment over time
    pos_pol = avg_polarity(pos)
    neg_pol = avg_polarity(neg)
    neu_pol = avg_polarity(neu)
    avg_pol = avg_polarity(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pos_pol.index, y=pos_pol,
        mode='lines',
        name='Positive'))
    fig.add_trace(go.Scatter(x=neu_pol.index, y=neu_pol,
        mode='lines',
        name='Neutral'))
    fig.add_trace(go.Scatter(x=neg_pol.index, y=neg_pol,
        mode='lines',
        name='Negative'))
    fig.add_trace(go.Scatter(x=avg_pol.index, y=avg_pol,
        mode='lines',
        name='Average'))
    fig.update_layout(
            title="Sentiment over Time",
            xaxis_title="Day",
            yaxis_title="Avg Polarity")
            #showlegend=False)
    return fig


def sentiment_proportions(df):
    pos = df[df["predicted-sentiment"]=="positive"]
    neg = df[df["predicted-sentiment"]=="negative"]
    neu = df[df["predicted-sentiment"]=="neutral"]

    values = [len(pos),len(neg),len(neu)]
    sent = ['Positive', 'Negative', 'Neutral']
    columns=['Sentiment', 'Number']
    sent_df = pd.DataFrame(list(zip(sent, values)), columns=columns)
    fig = px.pie(sent_df, values='Number', names='Sentiment', title='Sentiment Proportions')
    fig.update_layout(width=500, height=500)

    return fig


import os
import numpy as np
from time import time
from PIL import Image
from wordcloud import WordCloud
from stopwords import ENGLISH_STOP_WORDS

MASK_PATH = os.path.join(os.path.dirname(__file__), os.path.join("images", "twitter_mask.png"))
CLOUD_PATH = os.path.join(os.path.dirname(__file__), os.path.join("images"))

def tweet_cloud(tweets):
    stopwords = set(ENGLISH_STOP_WORDS)
    new_tweets = " ".join([tweet for tweet in tweets.split() if tweet not in stopwords])

    # create the word cloud
    mask = np.array(Image.open(MASK_PATH))
    wc = WordCloud(background_color="white",
        stopwords=stopwords,max_words=800,
        max_font_size=70, mask=mask).generate(new_tweets)
    # create new cloud image
    #image_name = "twitter_cloud_"+str(int(time()))+".png"
    image_name = "twitter_cloud.png"
    image_path = os.path.join(CLOUD_PATH, image_name)
    wc.to_file(image_path)
    return image_path
