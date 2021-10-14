from injector import inject, singleton
from flask import Flask

from controller.index_controller import IndexController
from controller.playlist_controller import PlaylistController
from controller.ranking_controller import RankingController
from controller.track_controller import TrackController


@singleton
class Router:
    @inject
    def __init__(
        self,
        app: Flask,
        index_controller: IndexController,
        track_controller: TrackController,
        ranking_controller: RankingController,
        playlist_controller: PlaylistController,
    ) -> None:
        self.app = app
        self.version = "v1"
        self.url_prefix = f"/api/{self.version}"

        self.index_controller = index_controller
        self.track_controller = track_controller
        self.ranking_controller = ranking_controller
        self.playlist_controller = playlist_controller

    def add_router(self):
        self.app.add_url_rule(
            rule="/",
            view_func=self.index_controller.get_index,
            methods=["GET"],
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/track",
            view_func=self.track_controller.get_tracks,
            methods=["GET"],
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/ranking",
            view_func=self.ranking_controller.get_ranking,
            methods=["GET"],
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/user/<uid>/playlist",
            view_func=self.playlist_controller.create_playlist,
            methods=["POST"],
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/user/<uid>/playlist",
            view_func=self.playlist_controller.get_playlist_infos,
            methods=["GET"],
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/user/<uid>/playlist/<playlist_id>",
            view_func=self.playlist_controller.get_playlist,
            methods=["GET"],
        )
        self.app.add_url_rule(
            rule=f"{self.url_prefix}/user/<uid>/playlist/<playlist_id>",
            view_func=self.playlist_controller.update_playlist,
            methods=["PUT"],
        )
        self.app.add_url_rule(
            rule=(
                f"{self.url_prefix}/user/<uid>/playlist/<playlist_id>"
                "/track/<playlist_track_id>"
            ),
            view_func=self.playlist_controller.delete_track,
            methods=["DELETE"],
        )
