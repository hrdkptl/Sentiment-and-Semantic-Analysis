import re
from pymongo import MongoClient
import json
import tweepy as tw
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#http://docs.tweepy.org/en/v3.5.0/api.html#help-methods
#https://medium.com/@swenushika/extracting-twitter-data-using-tweepy-a066d6e19be
#https://towardsdatascience.com/how-to-access-twitters-api-using-tweepy-5a13a206683b
#https://medium.com/@adam.oudad/stream-tweets-with-tweepy-in-python-99e85b6df468
#https://medium.com/@jaimezornoza/downloading-data-from-twitter-using-the-streaming-api-3ac6766ba96c
#https://stats.seandolinar.com/collecting-twitter-data-storing-tweets-in-mongodb/
#https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/
consumer_API_keys = "consumer_API_keys" #Replace this string with your key
consumer_API_secret_key = "consumer_API_secret_key" #Replace this string with your key
access_token = "access_token" #Replace this string with your key
access_token_secret = "access_token_secret" #Replace this string with your key

# # # CONNECT TO MONGODB # # #
client = MongoClient( 'localhost', 27017 )
db = client['Assignment_4']
collection = db['twitter_collection']
count = 0

# # # FUNCTION TO FETCH TWEEETS USING SEARCH API # # #
def Fetch_Tweets_SearchAPI():

    auth = tw.OAuthHandler( consumer_API_keys, consumer_API_secret_key )
    auth.set_access_token( access_token, access_token_secret )
    api = tw.API( auth, wait_on_rate_limit=True )

    keywords = '"Canada" OR "University" OR "Dalhousie University" OR "Halifax" OR "Canada Education"'

    tweets = tw.Cursor( api.search, q=keywords, lang="en", tweet_mode="extended").items( 8000 )

    for tweet in tweets:
        InsertToMongoDB(tweet._json)

# # # FUNCTION TO INSERT TWEETS TO MONGODB"
def InsertToMongoDB(data):
    global count
    count+=1
    collection.insert_one( data )
    print(count)

Fetch_Tweets_SearchAPI()
