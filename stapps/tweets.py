description = "Twitter Sentiment Analysis"

# Your app goes in the function run()
def run():
      import streamlit as st
      import snscrape.modules.twitter as sntwitter
      import pandas as pd
      import itertools
      import datetime
      from textblob import TextBlob
      import plots
      import re
      import math

      def clean(text):
            regExp = "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"
            return ' '.join(re.sub(regExp, " ", text).split())

      def sentiment(text):
            analysis = TextBlob(clean(text))
            polarity = analysis.sentiment.polarity
            result = ""
            if polarity > 0:
                  result = 'positive'
            elif polarity == 0:
                  result = 'neutral'
            else:
                  result = 'negative'
            return [result, math.floor(polarity * 100)]

      def subjectivity(text):
            return TextBlob(text).sentiment.subjectivity

      def polarity(text):
            return TextBlob(text).sentiment.polarity


      def as_df(query,start_date,end_date, max_tweets=200):
            # Initialize empty dataframe
            df = pd.DataFrame({
            'tweet': [],
            'clean_tweet': [],
            'predicted-sentiment': [],
            'polarity':[],
            'subjectivity':[],
            'date': []
            })
            search = query + " since:" + str(start_date) + " until:" + str(end_date)
            tweets = sntwitter.TwitterSearchScraper(search).get_items()
            # Add data for each tweet
            for tweet in itertools.islice(tweets, max_tweets):
                  # Skip iteration if tweet is empty
                  if tweet.content in ('', ' '):
                        continue
                  # Make predictions
                  sentence = clean(tweet.content)
                  psentiment, polarity = sentiment(sentence)
                  psubjectivity = subjectivity(sentence)

                  # Append new data
                  df = df.append({
                        'tweet': tweet.content,
                        'clean_tweet': sentence,
                        'predicted-sentiment': psentiment,
                        'polarity': polarity,
                        'subjectivity': psubjectivity,
                        'date': tweet.date}, ignore_index=True)
            df['date'] = pd.to_datetime(df['date']).dt.date
            return df

      st.title("Brandwatch")
      st.subheader('Search Twitter')
      st.info("A Twitter Sentiment analysis project which will scrap \
            twitter for the topic selected by the user. The extracted \
            tweets will then be used to determine the Sentiments of those \
            tweets. The different Visualizations will help us get a feel of the \
            overall mood of the people on Twitter regarding the topic we select.")

      # Get user input
      query = st.text_input('Query',value='')

      today = datetime.date.today()
      before = today - datetime.timedelta(days=100)
      start_date = st.date_input('Start date', before)
      end_date = st.date_input('End date', today)
      if start_date > end_date:
            st.error('Error: End date must fall after start date.')

      # As long as the query is valid (not empty or equal to '#')...
      if query != '' and query != '#':
            with st.spinner(f'Searching for and analysing {query}...'):
                  df = as_df(query, start_date, end_date)

                  col1, col2 = st.columns(2)
                  with col1:
                        fig = plots.sentiment_over_time(df)
                        st.plotly_chart(fig)

                        text = " ".join(tweet for tweet in df.clean_tweet)
                        st.image(plots.tweet_cloud(text))

                  with col2:
                        # daily volume
                        fig = plots.tweets_per_day(df)
                        st.plotly_chart(fig)

                        fig = plots.sentiment_proportions(df)
                        st.plotly_chart(fig)

# end of app

# This code allows you to run the app standalone
# as well as part of a library of apps
if __name__ == "__main__":
    run()
