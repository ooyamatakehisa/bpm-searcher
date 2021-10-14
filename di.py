from logging import Logger

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module
from redis import Redis

from interface.repository.access_token_repository import AccessTokenRepository
from interface.repository.auth_repository import AuthRepository
from interface.repository.playlist_repository import PlaylistRepository
from interface.repository.ranking_repository import RankingRepository
from interface.usecase.access_token_usecase import AccessTokenUsecase
from interface.usecase.auth_usecase import AuthUsecase
from interface.usecase.playlist_usecase import PlaylistUsecase
from interface.usecase.track_usecase import TrackUsecase
from interface.usecase.ranking_usecase import RankingUsecase
from interactor.access_token_interactor import AccessTokenInteractor
from interactor.auth_interactor import AuthInteractor
from interactor.playlist_interactor import PlaylistInteractor
from interactor.track_interactor import TrackInteractor
from interactor.ranking_interactor import RankingInteractor
from persistence.model import db
from persistence.access_token import AccessTokenRepositoryImpl
from persistence.auth import AuthRepositoryImpl
from persistence.playlist import PlaylistRepositoryImpl
from persistence.ranking import RankingRepositoryImpl


class DI(Module):
    def __init__(self, redis: Redis, app: Flask, logger: Logger):
        self.redis = redis
        self.app = app
        self.logger = logger

    def configure(self, binder):
        binder.bind(Flask, to=self.app)
        binder.bind(Logger, to=self.logger)
        binder.bind(Redis, to=self.redis)
        binder.bind(SQLAlchemy, to=db)
        binder.bind(AccessTokenRepository, to=AccessTokenRepositoryImpl)
        binder.bind(AuthRepository, to=AuthRepositoryImpl)
        binder.bind(PlaylistRepository, to=PlaylistRepositoryImpl)
        binder.bind(RankingRepository, to=RankingRepositoryImpl)
        binder.bind(AccessTokenUsecase, to=AccessTokenInteractor)
        binder.bind(AuthUsecase, to=AuthInteractor)
        binder.bind(PlaylistUsecase, to=PlaylistInteractor)
        binder.bind(RankingUsecase, to=RankingInteractor)
        binder.bind(TrackUsecase, to=TrackInteractor)
