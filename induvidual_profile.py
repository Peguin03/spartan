import tweepy
from keys import keys
import streamlit as st


def getProfile(user):
    twitter_keys = keys()

    # Setup access to API
    auth = tweepy.OAuthHandler(
    twitter_keys['consumer_key'],
    twitter_keys['consumer_secret'])
    auth.set_access_token(
    twitter_keys['access_token_key'],
    twitter_keys['access_token_secret'])

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
    
   
    
   



    
