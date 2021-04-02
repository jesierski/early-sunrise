import pyjokes
import requests
import config
import time
from sqlalchemy import create_engine


webhook_url = config.WEBHOOK_URL
    
time.sleep(10)

pg = create_engine('postgres://anja:anjapgpw@postgresdb:5432/anjapostgres_db', echo=True)


time.sleep(80)

while True:
    
    query = "SELECT text, sentiment FROM tweets ORDER BY timestamp DESC LIMIT 1;"

    text = 'Tweet: '+ pg.execute(query).first()[0] + '\nSentimentIntensityAnalyzer compound score: ' + str(pg.execute(query).first()[1]) + '\n(This score ranges from -1 to 1, where -1 is totally negative and +1 is totally positive): \n'
    data = {'text': text}
    requests.post(url=webhook_url, json = data)

    time.sleep(120)


