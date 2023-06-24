"""Endpoint to manage start and stopping of demo requests."""

import os
from datetime import datetime
from enum import Enum

from flask import jsonify, request
from flask.views import MethodView

from src import utils
from src.api.decorators import validate_token
from src.api.routes import _validate_args


class RequestType(Enum):
    START = 1
    END = 2

    @classmethod
    def valid_request_types(cls) -> set:
        return (cls.START.value, cls.END.value)


REQUIRED_GET_ARGS = ["megabase_user_key", "server_steam_id", "request_type"]
VALID_GET_ARGS = REQUIRED_GET_ARGS


class DemoManagerResource(MethodView):
    """API resource for managing demo start and end times from the client."""

    @validate_token
    def post(self):
        """Get channels for a given system and dataset."""
        kwargs = request.args.to_dict()
        validated = _validate_args(kwargs, REQUIRED_GET_ARGS, VALID_GET_ARGS)
        if validated is not None:
            return validated

        try:
            request_type = int(kwargs["request_type"])
            if request_type not in RequestType.valid_request_types():
                return jsonify(f"Expected request type to be one of {RequestType.valid_request_types()}"), 400

            # check if there is already an instance from this user (use key as this is 1-1 with steam id)
            megabase_user_key = kwargs["megabase_user_key"]
            server_steam_id = kwargs["server_steam_id"]
            is_active_session = utils.is_active_session(megabase_user_key)
            if is_active_session:
                return (
                    jsonify(
                        f"User is already actively in a session, please close it out before requesting a new session!"
                    ),
                    200,
                )

        except ValueError:
            return jsonify("Expected an integer!"), 400

        if request_type == RequestType.START:
            polling_session_id = utils.start_demo_session(megabase_user_key, server_steam_id)
            return jsonify(f"User started a session with {polling_session_id}!"), 200
        elif request_type == RequestType.END:
            if not is_active_session:
                return jsonify(f"User is not in a session, cannot close session out!"), 400
            polling_session_id = utils.stop_demo_session(megabase_user_key, server_steam_id)
            jsonify(f"User ended a session with {polling_session_id}!"), 200
