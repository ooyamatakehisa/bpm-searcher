from flask import jsonify, Response
from injector import inject, singleton

from interface.usecase.ranking_usecase import RankingUsecase


@singleton
class RankingController:
    @inject
    def __init__(self, ranking_usecase: RankingUsecase) -> None:
        self.ranking_usecase = ranking_usecase

    def get_ranking(self) -> Response:
        ranking = self.ranking_usecase.get_ranking()
        response = jsonify(ranking)
        response.cache_control.max_age = 60 * 60  # 1 hour
        return response
