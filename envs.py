import os

from injector import singleton


@singleton
class Envs:
    CLIENT_ID: str = os.environ["CLIENT_ID"]
    CLIENT_SECRET: str = os.environ["CLIENT_SECRET"]
    APP_ENV: str = os.environ["APP_ENV"]
    FIREBASE_PROJECT_ID: str = os.environ["FIREBASE_PROJECT_ID"]
    FIREBASE_CLIENT_EMAIL: str = os.environ["FIREBASE_CLIENT_EMAIL"]
    FIREBASE_PRIVATE_KEY: str = os.environ["FIREBASE_PRIVATE_KEY"]
    MYSQL_ADDR: str = os.environ["MYSQL_ADDR"]
    MYSQL_USER: str = os.environ["MYSQL_USER"]
    MYSQL_PASSWORD: str = os.environ["MYSQL_PASSWORD"]
    MYSQL_DATABASE: str = os.environ["MYSQL_DATABASE"]
