from keys import keys
import tweepy
import streamlit as st
import pandas as pd

def trends():
    twitter_keys = keys()

    # Setup access to API
    auth = tweepy.OAuthHandler(
    twitter_keys['consumer_key'],
    twitter_keys['consumer_secret'])
    auth.set_access_token(
    twitter_keys['access_token_key'],
    twitter_keys['access_token_secret'])

    api = tweepy.API(auth)

    res=api.trends_place(23424848)
    res=res[0]['trends']
    s='''
        Getting the trends by the location of India ,to get to know the latest political trends and issues and public interest.
        '''
    st.markdown(s)

    data={}

    for d in res:
        data[d['name']]=[d['name'],d['tweet_volume']]
    data=pd.DataFrame(data.values(),columns=['Name','Tweet Volume'])
    st.subheader('Trends')
    st.write('Data mined from Twitter')
    st.table(data)
