"""Utils for the API."""

from threading import Thread
from uuid import uuid4


def poll_server(steam_server_id: str) -> None:
    """Poll a server and send telemetry to the DB.

    Args:
        steam_server_id: ID of the server.
    """
    pass


class ServerPollingManager:
    """Class that handles polling servers with demo requests for server telemetry."""

    def __init__(self):
        self.active_sessions = {}
        self.id = uuid4().hex  # keep track in DB

    def start_session(self, steam_server_id: str) -> None:
        pass

    def close_session(self, steam_server_id: str) -> None:
        pass

    def poll_connections(self):
        """Poll the active connections table in the DB to make sure this instance is polling the correct servers."""
        pass
