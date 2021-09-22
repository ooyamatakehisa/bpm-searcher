import os


class Envs:
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
    APP_ENV: str = os.getenv("APP_ENV")
