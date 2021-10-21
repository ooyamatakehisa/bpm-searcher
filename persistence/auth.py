from logging import Logger

from firebase_admin import auth
from firebase_admin.exceptions import FirebaseError
from injector import inject, singleton

from interface.repository.auth_repository import AuthRepository


@singleton
class AuthRepositoryImpl(AuthRepository):
    @inject
    def __init__(self, logger: Logger):
        self.logger = logger

    def verify_user(self, id_token: str) -> dict:
        try:
            user = auth.verify_id_token(id_token)
            return user

        except FirebaseError as e:
            self.logger.error(f"invalid id token: {e}")
            return None
