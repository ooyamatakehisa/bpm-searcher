from injector import inject, singleton

from interface.repository.auth_repository import AuthRepository
from interface.usecase.auth_usecase import AuthUsecase


@singleton
class AuthInteractor(AuthUsecase):
    @inject
    def __init__(
        self,
        auth_repository: AuthRepository,
    ) -> None:
        self.auth_repository = auth_repository

    def verify_user(self, id_token: str) -> dict:
        user = self.auth_repository.verify_user(id_token)
        return user
