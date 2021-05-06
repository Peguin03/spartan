import tweepy
from keys import keys
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
from PIL import Image
import numpy as np
from collections import OrderedDict


class TweetsExtractor():

    def __init__(self):
        """
        Constructor function to setup the Twitter's API
        with our access keys provided.
        """

        # Authentication and access using keys:
        twitter_keys = keys()
        auth = tweepy.OAuthHandler(
                twitter_keys['consumer_key'],
                twitter_keys['consumer_secret'])
        auth.set_access_token(
                twitter_keys['access_token_key'],
                twitter_keys['access_token_secret'])


        # Return API with authentication:
        api = tweepy.API(auth)
        self.extractor = api

    def extract(self, user):
        """
        Function to extract latest 200 tweets from a
        user provided.
        """

        # We create a tweet list as follows:
        tweets = self.extractor.user_timeline(
                    screen_name=user,
                    count=500,
                    tweet_mode='extended')

        # Print number of tweets extracted:
        # print("Number of tweets extracted: {}.\n".format(len(tweets)))

        # We prepare data to create a dataframe:
        data = [[tw.full_text, len(tw.full_text), tw.id, tw.created_at,
                tw.source, tw.favorite_count, tw.retweet_count,
                tw.entities] for tw in tweets]
        columns = ['Tweets', 'len', 'ID', 'Date', 'Source',
                   'Likes', 'RTs', 'Entities']

        # We create a dataframe:
        dataframe = pd.DataFrame(data=data, columns=columns)

        return dataframe

class TweetsAnalyzer():

    def __init__(self, extractor):
        """
        Constructor function using a TweetsExtractor
        object.
        """

        # Construct object:
        self.extractor = extractor
        self.data = None
        self.hashtags = {}

        

    def analyze(self, user):
        """
        Analyzer function to gather all data from
        a TweetsExtractor object.
        """

        # Extract data from extractor:
        self.data = self.extractor.extract(user)

        # Construct hashtags dictionary:
        for entity in self.data['Entities']:
            if entity['hashtags']:
                for hashtag in entity['hashtags']:
                    if hashtag['text'] in self.hashtags.keys():
                        self.hashtags[hashtag['text']] += 1
                    else:
                        self.hashtags[hashtag['text']] = 1

        self.hashtags = OrderedDict(sorted(self.hashtags.items()))

        
    def top_hashtags(self, top=1e10):
        popular = sorted(self.hashtags.items(), key=lambda h: h[1], reverse=1)
        return popular[:top]

    def trending_tweets(self):
        """
        Utility funtion that returns the indices of
        the most popular tweets: the most liked and
        the most retweeted.
        """

        # We extract the tweet with more FAVs and more RTs:
        fav_max = max(self.data['Likes'])
        rt_max = max(self.data['RTs'])

        # Save the index of the first most liked and RT'd tweet:
        fav = self.data[self.data.Likes == fav_max].index[0]
        rt = self.data[self.data.RTs == rt_max].index[0]

        return fav, rt

class TweetsVisualizer():

    def __init__(self, analyzer):
        """
        Constructor function using a TweetsExtractor
        object.
        """

        # Construct object:
        self.analyzer = analyzer
        self.data = self.analyzer.data
        self.hashtags = self.analyzer.hashtags

        

    def retweets(self):
        """
        Function to plot time series of retweets.
        """

        # We create time series for data:
        data = self.data[['RTs', 'Date']]
        p = figure(title = 'Retweets along time',
                    x_axis_label = 'Date',
                    y_axis_label = 'Retweets',
                    sizing_mode = 'stretch_width',
                    x_axis_type='datetime',
                    max_width=750,
                    plot_height=250)

        p.line(data['Date'], data['RTs'], legend_label='Trend', line_width=2)
        st.bokeh_chart(p, use_container_width=True)
        p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

        
        
        

    def likes(self):
        """
        Function to plot time series of likes.
        """

        # We create time series for data:
        data = self.data[['Likes', 'Date']]
        p = figure(title = 'Likes along time',
                    x_axis_label = 'Date',
                    y_axis_label = 'Likes',
                    sizing_mode = 'stretch_width',
                    x_axis_type='datetime',
                    max_width=750,
                    plot_height=250)

        p.line(data['Date'], data['Likes'], legend_label='Trend', line_width=2)
        st.bokeh_chart(p, use_container_width=True)
        p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")
       
        

    def lengths(self):
        """
        Function to plot time series of lengths.
        """

        # We create time series for data:
        data = self.data[['len', 'Date']]
        p = figure(title = 'Length of Tweets along time',
                    x_axis_label = 'Date',
                    y_axis_label = 'Length of tweets',
                    sizing_mode = 'stretch_width',
                    x_axis_type='datetime',
                    max_width=750,
                    plot_height=250)

        p.line(data['Date'], data['len'], legend_label='Trend', line_width=2)
        st.bokeh_chart(p, use_container_width=True)
        p.xaxis[0].formatter = DatetimeTickFormatter(months="%b %Y")

        

    def create_mask(img_path, threshold=200):
        """
        Function to create a mask for word cloud.
        """
        def binarize_array(numpy_array, threshold=threshold):
            """Binarize a numpy array."""

            for i, _ in enumerate(numpy_array):
                for j, _ in enumerate(numpy_array[0]):
                    if numpy_array[i][j] > threshold:
                        numpy_array[i][j] = 255
                    else:
                        numpy_array[i][j] = 0
            return numpy_array

        def binarize_image(img_path, threshold=threshold):
            """Binarize an image."""

            image_file = Image.open(img_path)
            image = image_file.convert('L')
            image = np.array(image)
            image = binarize_array(image, threshold)

            return image

        return binarize_image(img_path, threshold=threshold)

    def wordcloud(self, mask=None):
        """
        Function to plot the wordloud with hashtags.
        """

        # Create text from hashtags:
        text = ' '.join(list(self.hashtags.keys()))

        # Create wordcloud:
        wordcloud = WordCloud(mask=mask, background_color="white",
                              scale=3, colormap="viridis")
        wordcloud.generate(text)

        # Plot figure:
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud, interpolation="bicubic")
        plt.margins(x=0, y=0)
        plt.axis("off")
        st.pyplot()



def getProfile(user):
    twitter_keys = keys()
    # twitter_keys = twitter_keys.keys
    # Setup access to API
    auth = tweepy.OAuthHandler(
    twitter_keys['consumer_key'],
    twitter_keys['consumer_secret'])
    auth.set_access_token(
    twitter_keys['access_token_key'],
    twitter_keys['access_token_secret'])

    s='''
        Basic data of the user entered is shown

        ### Workflow
            An influential rate is calculated based on a statistical formula.
            The rate is calculated by the ratio of number of followers of the user to total users in india ,this accounts for 75% of the score
            The rate is also influenced by the ratio of number of followers that the users followers have

            For Eg : Getting the top 25 followers of the user and finding thier influence.
            Accounting for the influence in 1st degree of seperation .This accounts for 25% of the score
        '''
    st.markdown(s)

    api = tweepy.API(auth)

    res = api.get_user(user)
    name = '''## Name ``` %s ``` ''' % (res.name)
    location = '''## Location ``` %s ``` ''' % (res.location)
    followers = '''## Followers ``` %s ``` ''' % (str(res.followers_count))
    friends = '''## Friends ``` %s ``` ''' % (str(res.friends_count))
    verified = '''## verified ``` %s ``` ''' % (str(res.verified))
    st.markdown(name)
    st.markdown(location)
    st.markdown(followers)
    st.markdown(friends)
    st.markdown(verified)

    user_followers=res.followers_count

    res=api.friends_ids(user)

    count=0;

    for i in range(0,25):
        user_data=api.get_user(res[i])
        count=count+user_data.followers_count

    users_num=300000000
    
    influential_rate=((user_followers/users_num)*0.75)+((count/users_num)*0.25)
    influence = '''## Influential Rate ``` %s ``` ''' % (str(influential_rate))
    
    st.markdown(influence)

    extractor = TweetsExtractor()
    analyzer = TweetsAnalyzer(extractor)
    analyzer.analyze(user)
    visualizer = TweetsVisualizer(analyzer)
    fav, rt = analyzer.trending_tweets()
    fav_tw = analyzer.data['Tweets'][fav]
    rt_tw = analyzer.data['Tweets'][rt]

    
    num_of_likes = '''## Number of Likes ``` %s ``` ''' % (str(analyzer.data['Likes'][fav]))
    num_retweets = '''## Number of retweets ``` %s ``` ''' % (str(analyzer.data['RTs'][rt]))
    st.markdown(num_of_likes)
    st.markdown(num_retweets)

    # st.write('**Number of Likes**: '+(str(analyzer.data['Likes'][fav])))
    # st.write('**Number of retweets**: '+ (str(analyzer.data['RTs'][rt])))
    st.write('**Most Liked Tweet**: '+ str(fav_tw))
    st.write('**Most Retweeted Tweet**: '+ (str(rt_tw)))
    

    # tweets_with_more_likes = '''## Tweets with More Likes ``` %s ``` ''' % (fav_tw)
    # num_of_likes = '''## Number of Likes ``` %s ``` ''' % (str(analyzer.data['Likes'][fav]))
    # more_retweets = '''## Tweet with more retweets is ``` %s ``` ''' % (str(rt_tw))
    # num_retweets = '''## Number of retweets ``` %s ``` ''' % (str(analyzer.data['RTs'][rt]))

    # st.markdown(tweets_with_more_likes)
    # st.markdown(num_of_likes)
    # st.markdown(more_retweets)
    # st.markdown(num_retweets)

    visualizer.lengths()
    visualizer.likes()
    visualizer.retweets()
    mask = visualizer.create_mask("twird.jpg")
    visualizer.wordcloud(mask)
    
