from flask import Blueprint

from src.api.routes.demo_manager import DemoManagerResource

api = Blueprint("api", __name__, url_prefix="/api")


api.add_url_rule(
    "/demomanager",
    methods=["POST"],
    view_func=DemoManagerResource.as_view("demomanager"),
)
