from flask import Flask, jsonify
import os
import requests
import tweepy

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'SIMP MAFIA TEST'


@app.route("/get-tweets/", methods=['GET'])
def get_tweet():
    bearer_token = os.environ['MY_BEARER_TOKEN']
    client = tweepy.Client(bearer_token=bearer_token)
    cm_tweet = client.get_users_tweets(id='930662549812600832')
    tweet1 = str(cm_tweet[0][0].id)
    tweet2 = str(cm_tweet[0][1].id)
    tweet3 = str(cm_tweet[0][2].id)
    lilb_tweet = client.get_users_tweets(id='37836873')
    tweet4 = str(lilb_tweet[0][0].id)
    jennie_tweet = client.get_users_tweets(id='3243685400')
    tweet5 = str(jennie_tweet[0][0].id)
    print(tweet1)

    tweets = {'CM Tweet 1': tweet1,
              'CM Tweet 2': tweet2,
              'CM Tweet 3': tweet3,
              'Lil B Tweet': tweet4,
              'Jennie Tweet': tweet5
              }
    data = jsonify(tweets)
    data.headers.add('Access-Control-Allow-Origin', '*')

    return data


@app.route("/get-data/", methods=['GET'])
def get_data():
    client_id = os.environ['MY_SECRET_SAUCE']
    client_secret = os.environ['MY_SECRET_ID']
    headers = {
        'Client-ID': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials',
        'Authorization': 'Bearer ' + os.environ['MY_SECRET_TOKEN']
    }
    streamers = ['cm_nyc_tv', 'gamerpool474_ph', 'snoozefighting', 'scentless__apprentice',
                 'mattnguyen', 'strawberriemlk', 'leyopan', 'camelul', 'replaisment']
    dicts = {}
    for streamer in streamers:
        url = "https://api.twitch.tv/helix/streams?user_login=" + streamer

        response = requests.get(url, headers=headers).json()
        # data output
        dicts[streamer] = len(response['data'])

    # data = json.dumps(dicts)
    data = jsonify(dicts)
    data.headers.add('Access-Control-Allow-Origin', '*')

    return data


if __name__ == '__main__':
    app.run()
