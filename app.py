import os

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


class DI(Module):
    def configure(self, binder):
        binder.bind(Flask, to=app)
        binder.bind(Logger, to=app.logger)
        binder.bind(Redis, to=redis)
        binder.bind(AccessTokenRepository, to=AccessTokenRepositoryImpl)
        binder.bind(RankingRepository, to=RankingRepositoryImpl)
        binder.bind(AccessTokenUsecase, to=AccessTokenInteractor)
        binder.bind(RankingUsecase, to=RankingInteractor)
        binder.bind(TrackUsecase, to=TrackInteractor)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://{envs.MYSQL_USER}:{envs.MYSQL_PASSWORD}@mysql/{envs.MYSQL_DATABASE}"
)
db.init_app(app)
migrate = Migrate(app, db)

injector = Injector([DI()])
router = injector.get(Router)
router.add_router()
