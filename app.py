from flask import Flask, render_template
import json
import os
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'SIMP MAFIA TEST'


@app.route("/get-data/")
def get_data():
    bearer_token = os.environ['MY_BEARER_TOKEN']

    client_id = os.environ['MY_SECRET_SAUCE']
    client_secret = os.environ['MY_SECRET_ID']
    headers = {
        'Client-ID': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials',
        'Authorization': 'Bearer ' + os.environ['MY_SECRET_TOKEN']
    }
    streamers = ['cm_nyc_tv', 'gamerpool474_ph', 'snoozefighting', 'scentless__apprentice',
                 'mattnguyen', 'leyopan', 'camelul', 'replaisment']
    dicts = {}
    for streamer in streamers:
        url = "https://api.twitch.tv/helix/streams?user_login=" + streamer

        response = requests.get(url, headers=headers).json()
        # data output
        dicts[streamer] = len(response['data'])

    data = json.dumps(dicts)

    return render_template("index.html", data=data,)



if __name__ == '__main__':
    app.run()
