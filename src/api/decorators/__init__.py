from functools import wraps

from flask import jsonify, request


def is_valid_megabase_key(key: str) -> bool:
    """Perform some bs lookup eventually to validate this."""
    return True


def validate_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        """Verifies megabase api key header."""
        for k in request.args.keys():
            if k.lower() == "megabase_user_key":
                key = request.args.get("megabase_user_key")
                break
            else:
                return jsonify("Unauthorized"), 401

        if is_valid_megabase_key(key):  # TODO implement
            return f(*args, **kwargs)

        else:
            return jsonify("Invalid megabase key"), 400

    return wrapper
