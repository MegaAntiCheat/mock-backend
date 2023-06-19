"""Endpoint to manage start and stopping of demo requests."""

import os
from datetime import datetime
from enum import Enum

from flask import jsonify, request
from flask.views import MethodView

from src.api.decorators import validate_token
from src.api.routes import _validate_args


class RequestType(Enum):
    START = 1
    END = 2


REQUIRED_GET_ARGS = ["server_steam_id", "request_type"]
VALID_GET_ARGS = REQUIRED_GET_ARGS


class DemoManagerResource(MethodView):
    """API resource for managing demo start and end times from the client."""

    @validate_token
    def get(self):
        """Get channels for a given system and dataset."""
        kwargs = request.args.to_dict()
        validated = _validate_args(kwargs, REQUIRED_GET_ARGS, VALID_GET_ARGS)
        if validated is not None:
            return validated

        try:
            server_steam_id = kwargs["server_steam_id"]
            request_type = int(kwargs["request_type"])
        except ValueError:
            return jsonify("Expected an integer!"), 400

        if request_type == RequestType.START:
            # TODO start polling the server the user is on...
            return jsonify(f"Starting server poll worker on {server_steam_id=}"), 200
        elif request_type == RequestType.END:
            # TODO stop polling the server the user is on...
            jsonify(f"Stopping server poll worker on {server_steam_id=}"), 200
