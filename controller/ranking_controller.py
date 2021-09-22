from flask import jsonify, Response
from injector import inject

from interface.usecase.ranking_usecase import RankingUsecase


class RankingController:
    @inject
    def __init__(self, ranking_usecase: RankingUsecase) -> None:
        self.ranking_usecase = ranking_usecase

    def get_ranking(self) -> Response:
        ranking = self.ranking_usecase.get_ranking()
        return jsonify(ranking)
