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


@app.route("/follower-counts/", methods=['GET'])
def get_follower_counts():
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
                 'FaruIRL', 'Domorobogato', 'babubird', 'stinkycarnival', 'commandercooder', 'hazelbunni', 'luxcess',
                 'ulumaika', 'tikitacotony', 'KozyBean', 'aznricecakes', 'Koi_ana', 'Mysterium0619']
    follower_data = {}

    for streamer in streamers:
        # Step 1: Get the User ID for the streamer name
        user_url = f"https://api.twitch.tv/helix/users?login={streamer}"
        user_resp = requests.get(user_url, headers=headers).json()

        if 'data' in user_resp and len(user_resp['data']) > 0:
            user_id = user_resp['data'][0]['id']

            # Step 2: Get the follower count using that User ID
            # This endpoint returns a 'total' field which is exactly what we need
            follow_url = f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}"
            follow_resp = requests.get(follow_url, headers=headers).json()

            follower_data[streamer] = follow_resp.get('total', 0)
        else:
            follower_data[streamer] = "User not found"

    response = jsonify(follower_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/follower-counts2/", methods=['GET'])
def get_follower_counts2():
    headers = {
        'Client-ID': os.environ['MY_CLIENT_ID'],
        'Authorization': 'Bearer ' + os.environ['MY_AUTHORIZATION']
    }

    streamers = ['cm_nyc', 'snoozefighting', 'scentless_apprentice', 'Rinzson', 'extrahotchicken', 'clearjoker',
                 'chato__', 'keokeofofeo', 'crispyjenny', 'mommygivememilk', 'philski', 'sattamxSAM',
                 'FaruIRL', 'Domorobogato', 'babubird', 'stinkycarnival', 'commandercooder', 'hazelbunni', 'luxcess',
                 'ulumaika', 'tikitacotony', 'KozyBean', 'aznricecakes', 'Koi_ana', 'Mysterium0619']

    # --- STEP 1: Get all User IDs in ONE request (Insta-method style) ---
    query = '&login='.join(streamers)
    user_url = f"https://api.twitch.tv/helix/users?login={query}"
    user_data = requests.get(user_url, headers=headers).json()

    # Create a mapping of Login Name -> User ID
    name_to_id = {user['login']: user['id'] for user in user_data['data']}

    # --- STEP 2: Get follower totals ---
    final_stats = {}
    for streamer in streamers:
        user_id = name_to_id.get(streamer.lower())
        if user_id:
            # Note: This part MUST be one-by-one (Twitch limitation)
            f_url = f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={user_id}"
            f_resp = requests.get(f_url, headers=headers).json()
            final_stats[streamer] = f_resp.get('total', 0)
        else:
            final_stats[streamer] = 0

    data = jsonify(final_stats)
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
                 'FaruIRL', 'Domorobogato', 'babubird', 'stinkycarnival', 'commandercooder', 'hazelbunni', 'luxcess', 'ulumaika', 'tikitacotony', 'KozyBean', 'aznricecakes', 'Koi_ana', 'Mysterium0619', 'prettygoodgaming_']
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
