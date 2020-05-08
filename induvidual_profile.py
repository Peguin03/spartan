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


        
    
   
    
   



    
