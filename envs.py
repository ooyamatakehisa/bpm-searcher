import os

from injector import singleton


@singleton
class Envs:
    CLIENT_ID: str = os.environ["CLIENT_ID"]
    CLIENT_SECRET: str = os.environ["CLIENT_SECRET"]
    APP_ENV: str = os.environ["APP_ENV"]
    MYSQL_USER: str = os.environ["MYSQL_USER"]
    MYSQL_PASSWORD: str = os.environ["MYSQL_PASSWORD"]
    MYSQL_DATABASE: str = os.environ["MYSQL_DATABASE"]
