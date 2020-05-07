from keys import keys
import tweepy

twitter_keys = keys()

auth = tweepy.OAuthHandler(
twitter_keys['consumer_key'],
twitter_keys['consumer_secret'])
auth.set_access_token(
twitter_keys['access_token_key'],
twitter_keys['access_token_secret'])

api = tweepy.API(auth)

res=api.search(q='*',count=20)
# for tweet in res:
#     print(tweet.text)

print(api.get_user('narendramodi'))
print(res)