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