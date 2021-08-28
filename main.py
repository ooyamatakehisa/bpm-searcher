import os

import requests
from requests.auth import HTTPBasicAuth
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(
    __name__,
    static_url_path="",
    static_folder="bpm-searcher-frontend/build",
    template_folder="bpm-searcher-frontend/build",
)
CORS(app)


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def search():
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
    
    response = requests.get(
        f"https://api.spotify.com/v1/audio-features",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "ids": ",".join(map(lambda item: item["id"], items)),
        },
    )

    features = response.json()["audio_features"]

    ret = []
    for idx, item in enumerate(items):
        spotify_id = item["id"]
        song_name = item["name"]
        artist = item["artists"][0]["name"]
        image_url = item["album"]["images"][0]["url"]
        album_name = item["album"]["name"]
        preview_url = item["preview_url"]

        ret.append({
            "spotify_id": spotify_id,
            "song_name": song_name,
            "album_name": album_name,
            "artist": artist,
            "bpm": features[idx]["tempo"],
            "key": features[idx]["key"],
            "image_url": image_url,
            "preview_url": preview_url,
            "danceability": features[idx]["danceability"],
            "energy": features[idx]["energy"],
        })

    return jsonify(ret)