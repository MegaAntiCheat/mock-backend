from functools import wraps

from flask import jsonify, request


def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        """Verifies megabase api key header."""
        for k in request.headers.keys():
            if k.lower() == "megabase_key":
                key = request.headers.get("megabase_key")
                break
            else:
                return jsonify("Unauthorized"), 401

        if is_valid_megabase_key(key):  # TODO implement
            return f(*args, **kwargs)

        else:
            return jsonify("Invalid megabase key"), 400

    return wrapper
