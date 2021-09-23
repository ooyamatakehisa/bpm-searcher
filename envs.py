import os


class Envs:
    CLIENT_ID: str = os.environ["CLIENT_ID"]
    CLIENT_SECRET: str = os.environ["CLIENT_SECRET"]
    APP_ENV: str = os.environ["APP_ENV"]
