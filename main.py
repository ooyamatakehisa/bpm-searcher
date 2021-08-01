import base64

import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify

app = Flask(__name__)

CLIENT_ID = "12f045556f09486ba2ca641e0f062fa0"
CLIENT_SECRET = "db8aa873758144bd8dd5b575412921bf"


@app.route("/")
def hello_world():
    auth = base64.b64encode(str.encode(f"{CLIENT_ID}:{CLIENT_SECRET}"))
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
    )
    access_token = response.json()["access_token"]

    query = request.args.get("search")
    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "type": "track",
            "q": query,
        },
    )

    items = response.json()["tracks"]["items"]
    if len(items) == 0:
        return "", 400

    ret = []
    for item in items:
        spotify_id = item["id"]
        song_name = item["name"]
        artist = item["artists"][0]["name"]

        response = requests.get(
            f"https://api.spotify.com/v1/audio-features/{spotify_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        bpm = response.json()["tempo"]
        ret.append({
            "song": song_name,
            "artist": artist,
            "bpm": bpm,
        })

    return jsonify(ret)