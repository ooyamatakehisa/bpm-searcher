from injector import inject
from flask import Flask

from controller.index_controller import IndexController
from controller.ranking_controller import RankingController
from controller.track_controller import TrackController


class Router:
    @inject
    def __init__(
        self,
        app: Flask,
        index_controller: IndexController,
        track_controller: TrackController,
        ranking_controller: RankingController,
    ) -> None:
        self.app = app
        self.version = ""
        self.url_prefix = f"/api/{self.version}"

        self.index_controller = index_controller
        self.track_controller = track_controller
        self.ranking_controller = ranking_controller

    def add_router(self):
        self.app.add_url_rule(
            rule="/",
            view_func=self.index_controller.get_index
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}",
            # rule=f"{self.url_prefix}/track",
            view_func=self.track_controller.get_tracks
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/ranking",
            view_func=self.ranking_controller.get_ranking
        )
