from dataclasses import asdict

from flask import jsonify, make_response, Response, request
from injector import inject, singleton

from interface.usecase.playlist_usecase import PlaylistUsecase
from interface.usecase.auth_usecase import AuthUsecase


@singleton
class PlaylistController:
    @inject
    def __init__(
        self,
        playlist_usecase: PlaylistUsecase,
        auth_usecase: AuthUsecase
    ) -> None:
        self.playlist_usecase = playlist_usecase
        self.auth_usecase = auth_usecase

    def create_playlist(self, uid: str):
        headers = request.headers
        bearer = headers.get("Authorization")
        if bearer is None:
            return make_response("no id token is specified", 401)

        bearer = bearer.split()
        if len(bearer) != 2:
            return make_response("beaer header is invalid format", 401)

        id_token = bearer[1]
        user = self.auth_usecase.verify_user(id_token)
        if user is None:
            return make_response("invalid id token", 401)

        if user["uid"] != uid:
            return make_response("uid in path param is incorrect", 403)

        body = request.get_json()
        if body is None:
            return make_response("content type must be application/json", 400)

        if "name" not in body or "desc" not in body:
            return make_response("'name' and 'desc' key must be specified", 400)

        name = body["name"]
        desc = body["desc"]
        playlist_info = self.playlist_usecase.create_playlist(name, desc, uid)
        return jsonify(asdict(playlist_info))

    def get_playlist(self, uid: str, playlist_id: str) -> Response:
        headers = request.headers
        bearer = headers.get("Authorization")
        if bearer is None:
            return make_response("no id token is specified", 401)

        bearer = bearer.split()
        if len(bearer) != 2:
            return make_response("beaer header is invalid format", 401)

        id_token = bearer[1]
        user = self.auth_usecase.verify_user(id_token)
        if user is None:
            return make_response("invalid id token", 401)

        if user["uid"] != uid:
            return make_response("uid in path param is incorrect", 403)

        playlist = self.playlist_usecase.get_playlist(playlist_id)
        if playlist is None:
            return make_response("playlist with the specified id does not exist", 404)

        return jsonify(playlist)

    def get_playlist_infos(self, uid: str) -> Response:
        headers = request.headers
        bearer = headers.get("Authorization")
        if bearer is None:
            return make_response("no id token is specified", 401)

        bearer = bearer.split()
        if len(bearer) != 2:
            return make_response("beaer header is invalid format", 401)

        id_token = bearer[1]
        user = self.auth_usecase.verify_user(id_token)
        if user is None:
            return make_response("invalid id token", 401)

        if user["uid"] != uid:
            return make_response("uid in path param is incorrect", 403)

        playlist_infos = self.playlist_usecase.get_playlist_infos(uid)
        plyalist_infos = [asdict(playlist_info) for playlist_info in playlist_infos]
        return jsonify(plyalist_infos)

    def update_playlist(self, uid: str, playlist_id: str) -> Response:
        headers = request.headers
        bearer = headers.get("Authorization")
        if bearer is None:
            return make_response("no id token is specified", 401)

        bearer = bearer.split()
        if len(bearer) != 2:
            return make_response("beaer header is invalid format", 401)

        id_token = bearer[1]
        user = self.auth_usecase.verify_user(id_token)
        if user is None:
            return make_response("invalid id token", 401)

        if user["uid"] != uid:
            return make_response("uid in path param is incorrect", 403)

        body = request.get_json()
        if body is None:
            return make_response("content type must be application/json", 400)

        if "kind" not in body:
            return make_response("'kind' key must be specified", 400)

        if body["kind"] == "info":
            if not all([e in body for e in ["name", "desc"]]):
                return make_response("'name' and 'desc' key must be specified", 400)

            playlist_info = self.playlist_usecase.update_playlist(
                kind=body["kind"],
                playlist_id=playlist_id,
                name=body["name"],
                desc=body["desc"],
            )
            if playlist_info is None:
                return make_response("playlist does not exist", 404)

        elif body["kind"] == "track":
            if "spotify_id" not in body:
                message = "'spotify_id' key must be specified"
                return make_response(message, 400)

            playlist = self.playlist_usecase.update_playlist(
                kind=body["kind"],
                playlist_id=playlist_id,
                spotify_id=body["spotify_id"],
            )
            if playlist is None:
                return make_response("playlist does not exist", 404)

        else:
            return make_response("'kind' key must be either 'info' or 'track'", 400)

        return make_response("update playlist", 200)

    def delete_playlist(self, uid: str, playlist_id: str) -> Response:
        headers = request.headers
        bearer = headers.get("Authorization")
        if bearer is None:
            return make_response("no id token is specified", 401)

        bearer = bearer.split()
        if len(bearer) != 2:
            return make_response("beaer header is invalid format", 401)

        id_token = bearer[1]
        user = self.auth_usecase.verify_user(id_token)
        if user is None:
            return make_response("invalid id token", 401)

        if user["uid"] != uid:
            return make_response("uid in path param is incorrect", 403)

        playlist_info = self.playlist_usecase.delete_playlist(playlist_id)
        if playlist_info is None:
            return make_response("playlist with the specified id does not exist", 404)

        return make_response("delete playlist", 204)

    def delete_track(
        self,
        uid: str,
        playlist_id: str,
        playlist_track_id: str
    ) -> Response:
        headers = request.headers
        bearer = headers.get("Authorization")
        if bearer is None:
            return make_response("no id token is specified", 401)

        bearer = bearer.split()
        if len(bearer) != 2:
            return make_response("beaer header is invalid format", 401)

        id_token = bearer[1]
        user = self.auth_usecase.verify_user(id_token)
        if user is None:
            return make_response("invalid id token", 401)

        if user["uid"] != uid:
            return make_response("uid in path param is incorrect", 403)

        playlist = self.playlist_usecase.delete_track(playlist_id, playlist_track_id)
        if playlist is None:
            return make_response("specified track or playlist does not exist", 404)

        return make_response("delete playlist", 204)
