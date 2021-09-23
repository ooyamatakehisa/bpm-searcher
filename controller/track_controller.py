from flask import request, jsonify, Response
from injector import inject, singleton

from interface.usecase.track_usecase import TrackUsecase


@singleton
class TrackController:
    @inject
    def __init__(self, track_usecase: TrackUsecase):
        self.track_usecase = track_usecase

    def get_tracks(self) -> Response:
        query = request.args.get("search")
        tracks = self.track_usecase.get_tracks(query)
        if len(tracks) == 0:
            return "", 404
        return jsonify(tracks)
