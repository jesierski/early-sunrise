import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

time.sleep(10)  # seconds

client = pymongo.MongoClient('mongodb')
db = client.tweet_collector

pg = create_engine('postgres://anja:anjapgpw@postgresdb:5432/anjapostgres_db', echo=True)

pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    timestamp BIGINT, 
    text VARCHAR(500),
    sentiment NUMERIC
);
''')

while True:

    entries = db.tweets.find()
    for e in entries:
        timestamp = e['timestamp_ms']
        text = e['text']
        s = SentimentIntensityAnalyzer()
        score = s.polarity_scores(text)['compound']  # compound vader value
        query = 'INSERT INTO tweets VALUES (%s, %s, %s);'
        pg.execute(query, (timestamp, text, score))

    time.sleep(30)


