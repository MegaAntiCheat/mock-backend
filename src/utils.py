"""Utils for the API."""

import os
from datetime import datetime, timezone
from threading import Thread
from uuid import uuid4

import sqlalchemy as sa

from src.db.models import PollingSession

DATABASE_URL = os.getenv("DATABASE_URL", None)
if DATABASE_URL is not None:
    engine = sa.create_engine(DATABASE_URL)
    Session = sa.orm.sessionmaker(engine)
else:
    engine = None
    Session = None


def is_active_session(megabase_user_key: str) -> bool:
    with Session() as session:
        sql = sa.select(PollingSession).where(
            PollingSession.megabase_user_key == "megabase_user_key", PollingSession.is_active == True
        )
        _is_active_session = session.execute(sql).scalar_one_or_none()

        if _is_active_session is None:
            return False

        return True


def start_demo_session(megabase_user_key: str, server_steam_id: str):
    try:
        server_steamid64 = int(server_steam_id)
    except ValueError:
        server_steamid64 = convert_server_id3_id_to_64_id(server_steam_id)

    polling_session_id = uuid4().hex
    start_time = datetime.now().astimezone(timezone.utc)
    with Session() as session:
        polling_session = PollingSession(
            polling_session_id=polling_session_id,
            megabase_user_key=megabase_user_key,
            server_steamid64=server_steamid64,
            is_active=True,
            start_time=start_time,
        )
        session.add(polling_session)
        session.commit()

    return polling_session_id


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


SERVER_STEAM_ID_MAPPING = {
    "I": 0,  # Invalid
    "i": 0,  # Invalid
    "U": 1,  # Individual
    "M": 2,  # Multiseat
    "G": 3,  # GameServer
    "A": 4,  # AnonGameServer
    "P": 5,  # Pending
    "C": 6,  # ContentServer
    "g": 7,  # Clan
    "T": 8,  # Chat
    "L": 8,  # Chat
    "c": 8,  # Chat
    "a": 10,  # AnonUser
}


def convert_server_id3_id_to_64_id(id3: str) -> str:
    """Convert a server id3 id to 64 id.

    Args:
        id3: server id3 str like [A:1:658635804:23591]

    Returns:
        converted id as a string
    """

    def _num_bin(num, size):
        if num >= pow(2, size):
            raise ValueError("'num' is out of bounds!")
        return bin(num)[2:].zfill(size)

    if id3[0].startswith("["):
        id3 = id3[1:]

    if id3[-1].endswith("]"):
        id3 = id3[:-1]

    parts = id3.split(":")

    type_id = SERVER_STEAM_ID_MAPPING[parts[0]]
    universe = int(parts[1])
    account_id = int(parts[2])
    if len(parts) >= 4:
        instance_id = int(parts[3])
    else:
        raise ValueError("'convert_server_id3_id_to_64_id' can only convert server ids!")

    id_bin = f"{_num_bin(universe, 8)}{_num_bin(type_id, 4)}{_num_bin(instance_id, 20)}{_num_bin(account_id, 32)}"

    steam64_id = int(id_bin, 2)

    return str(steam64_id)
