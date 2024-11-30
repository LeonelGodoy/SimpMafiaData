from flask import Flask, jsonify
import os
import requests

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
    streamers = ['cm_nyc_tv', 'gamerpool474_ph', 'snoozefighting', 'scentless__apprentice',
                 'mattnguyen', 'chato__', 'chefiejay', 'camelul', 'crispyjenny']
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



if __name__ == '__main__':
    app.run()
