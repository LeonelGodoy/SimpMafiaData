from flask import Flask, jsonify
import os
import requests
import json
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'SIMP MAFIA TEST'

@app.route("/get-data/", methods=['GET'])
def get_data():
    client_id = os.environ['MY_CLIENT_ID']
    client_secret = os.environ['MY_CLIENT_SECRET']
    headers = {
        'Client-ID': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials',
        'Authorization': 'Bearer ' + os.environ['MY_AUTHORIZATION']
    }
    streamers = ['cm_nyc', 'snoozefighting', 'scentless_apprentice', 'Rinzson', 'extrahotchicken', 'clearjoker',
                 'mattnguyen', 'chato__', 'keokeofofeo', 'crispyjenny', 'mommygivememilk', 'philski', 'sattamxSAM', 'FaruIRL', 'Domorobogato']
    dicts = {}
    for streamer in streamers:
        url = "https://api.twitch.tv/helix/streams?user_login=" + streamer
        print(url)

        response = requests.get(url, headers=headers).json()
        print(response)
        # data output
        dicts[streamer] = len(response['data'])

    # data = json.dumps(dicts)
    data = jsonify(dicts)
    data.headers.add('Access-Control-Allow-Origin', '*')

    return data


@app.route("/streamers/", methods=['GET'])
def streamer():
    client_id = os.environ['MY_CLIENT_ID']
    client_secret = os.environ['MY_CLIENT_SECRET']
    # Assume 'headers' is already defined
    headers = {
        'Client-ID': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials',
        'Authorization': 'Bearer ' + os.environ['MY_AUTHORIZATION']
    }
    # A list of up to 100 streamer logins
    streamers = ['cm_nyc', 'snoozefighting', 'scentless_apprentice', 'Rinzson', 'extrahotchicken', 'clearjoker',
                 'chato__', 'keokeofofeo', 'crispyjenny', 'mommygivememilk', 'philski', 'sattamxSAM',
                 'FaruIRL', 'Domorobogato', 'babubird', 'stinkycarnival', 'commandercooder', 'hazelbunni', 'luxcess']
    dicts = {}

    # Create the URL query string by joining streamer names
    query = '&user_login='.join(streamers)
    url = "https://api.twitch.tv/helix/streams?user_login=" + query
    print(url)

    response = requests.get(url, headers=headers).json()
    print(response)
    # Create a set of live streamers from the response for quick lookups
    live_streamers = {stream['user_login'].lower() for stream in response['data']}

    # Check which of your requested streamers are live
    for streamer in streamers:
        # A streamer is live if their lowercase login is in the live_streamers set
        dicts[streamer] = 1 if streamer.lower() in live_streamers else 0

    # data = json.dumps(dicts)
    # data = json.dumps(dicts)
    data = jsonify(dicts)
    data.headers.add('Access-Control-Allow-Origin', '*')


    return data



if __name__ == '__main__':
    app.run()
