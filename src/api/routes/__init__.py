from flask import jsonify


def _validate_args(request: dict[str, str], required_args: list[str], valid_args: list[str]) -> None:
    if missing_fields := set(required_args).difference(set(request.keys())):
        return jsonify(f"Bad request: missing required fields: {missing_fields}"), 400
    for k in request.keys():
        if k not in valid_args:
            return jsonify(f"Bad request: '{k}' is an invalid field"), 400
