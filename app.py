import os

from injector import Injector, Module
from flask import Flask
from flask_cors import CORS
import redis
from redis import Redis

from envs import Envs
from interface.repository.access_token_repository import AccessTokenRepository
from interface.repository.ranking_repository import RankingRepository
from interface.usecase.track_usecase import TrackUsecase
from interface.usecase.ranking_usecase import RankingUsecase
from interactor.track_interactor import TrackInteractor
from interactor.ranking_interactor import RankingInteractor
from persistence.access_token import AccessTokenRepositoryImpl
from persistence.ranking import RankingRepositoryImpl
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
        # binder.bind(Envs, to=envs)
        binder.bind(Redis, to=redis)
        binder.bind(AccessTokenRepository, to=AccessTokenRepositoryImpl)
        binder.bind(RankingRepository, to=RankingRepositoryImpl)
        binder.bind(RankingUsecase, to=RankingInteractor)
        binder.bind(TrackUsecase, to=TrackInteractor)


injector = Injector([DI()])
router = injector.get(Router)
router.add_router()
