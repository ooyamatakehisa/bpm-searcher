import os
import time

import redis
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

APP_ENV = os.getenv("APP_ENV")

if APP_ENV == "DEV":
    kwargs = {
        "url": os.environ.get('REDIS_URL'),
        "decode_responses": True,
    }
elif APP_ENV == "PRD":
    kwargs = {
        "url": os.environ.get('REDIS_TLS_URL'),
        "decode_responses": True,
        "ssl_cert_reqs": None,
    }
redis = redis.from_url(**kwargs)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api")
def search():
    if is_valid_access_token(redis):
        app.logger.info("valid")
        access_token = get_spotify_access_token(redis)
    else:
        app.logger.info("invalid")
        access_token = create_spotify_access_token(redis)

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
        return "", 404

    response = requests.get(
        "https://api.spotify.com/v1/audio-features",
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


@app.route("/api/ranking")
def ranking():
    if is_valid_access_token(redis):
        app.logger.info("valid")
        access_token = get_spotify_access_token(redis)
    else:
        app.logger.info("invalid")
        access_token = create_spotify_access_token(redis)

    global_charts_id = "37i9dQZEVXbMDoHDwVN2tF"
    response = requests.get(
        f"https://api.spotify.com/v1/playlists/{global_charts_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    items = response.json()["tracks"]["items"]

    response = requests.get(
        "https://api.spotify.com/v1/audio-features",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "ids": ",".join(map(lambda item: item["track"]["id"], items)),
        },
    )

    features = response.json()["audio_features"]

    ret = []
    for idx, item in enumerate(items):
        spotify_id = item["track"]["id"]
        song_name = item["track"]["name"]
        artist = item["track"]["artists"][0]["name"]
        image_url = item["track"]["album"]["images"][0]["url"]
        album_name = item["track"]["album"]["name"]
        preview_url = item["track"]["preview_url"]

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


def create_spotify_access_token(redis):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={"grant_type": "client_credentials"},
    )
    access_token = response.json()["access_token"]

    # spotify access token will expire after 1 hour and set ttl to 50 minutes
    ttl = time.time() + 60 * 50
    dict_ = {"access_token": access_token, "ttl": ttl}
    redis.hmset("access_token", dict_)
    return access_token


def is_valid_access_token(redis):
    exists = redis.exists("access_token")
    return exists and float(redis.hget("access_token", "ttl")) > time.time()


def get_spotify_access_token(redis):
    return redis.hget("access_token", "access_token")
