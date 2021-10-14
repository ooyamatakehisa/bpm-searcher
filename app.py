import os

import firebase_admin
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import redis
from redis import Redis

from envs import Envs
from persistence.model import db
from router import Router


app = Flask(
    __name__,
    static_url_path="",
    static_folder="bpm-searcher-frontend/build",
    template_folder="bpm-searcher-frontend/build",
)
CORS(app)

envs = Envs()

if envs.APP_ENV == "DEV":
    kwargs = {
        "url": os.environ.get('REDIS_URL'),
        "decode_responses": True,
    }
elif envs.APP_ENV == "PRD":
    kwargs = {
        "url": os.environ.get('REDIS_TLS_URL'),
        "decode_responses": True,
        "ssl_cert_reqs": None,
    }

redis = redis.from_url(**kwargs)

cred = firebase_admin.credentials.Certificate({
    "type": "service_account",
    "project_id": envs.FIREBASE_PROJECT_ID,
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_email": envs.FIREBASE_CLIENT_EMAIL,
    "private_key": envs.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
})
firebase_admin.initialize_app(cred)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://{envs.MYSQL_USER}:{envs.MYSQL_PASSWORD}@mysql/{envs.MYSQL_DATABASE}"
)
db.init_app(app)
migrate = Migrate(app, db)

injector = Injector([DI()])
router = injector.get(Router)
router.add_router()
