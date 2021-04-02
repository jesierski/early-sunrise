import config
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json
import logging
import pymongo

# connect to MongoDB server
client = pymongo.MongoClient('mongodb')

# create/use a database
db = client.tweet_collector

# define the collection
collection = db.tweets

#I didn't get this to work
# get environment variables
#TWITTER_API_KEY = os.getenv('TWITTER_CONSUMER_API_KEY')
#TWITTER_API_SECRET = os.getenv('TWITTER_CONSUMER_API_SECRET')
#TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
#TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

def authenticate():
    """Function for handling Twitter Authentication. Please note
       that this script assumes you have a file called config.py
       which stores the 4 required authentication tokens:

       1. API_KEY
       2. API_SECRET
       3. ACCESS_TOKEN
       4. ACCESS_TOKEN_SECRET

    See course material for instructions on getting your own Twitter credentials.
    """
    auth = OAuthHandler(config.API_KEY, config.API_SECRET)
    auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

    return auth

class TwitterListener(StreamListener):

    def on_data(self, data):

        """Whatever we put in this method defines what is done with
        every single tweet as it is intercepted in real-time"""

        t = json.loads(data) #t is just a regular python dictionary.

        tweet = {
        'text': t['text'],
        'username': t['user']['screen_name'],
        'followers_count': t['user']['followers_count'],
        'timestamp_ms': int(t['timestamp_ms'])
        }

        logging.critical(f'\n\n\nTWEET INCOMING: {tweet["text"]}\n\n\n')
        
        # write tweets into MongoDB database tweet_collector, collection tweets
        collection.insert_one(tweet)

    def on_error(self, status):

        if status == 420:
            print(status)
            return False

if __name__ == '__main__':

    auth = authenticate()
    listener = TwitterListener()
    stream = Stream(auth, listener)
    message = stream.filter(track=['Angela Merkel'], languages=['en'])
