from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Report(Base):
    __tablename__ = "reports"

    upload_time = sa.Column("upload_time", sa.types.TIMESTAMP(timezone=True), primary_key=True)
    reporter_steam_id = sa.Column("reporter_steam_id", sa.String, primary_key=True)
    suspected_cheater_steam_id = sa.Column("suspected_cheater_steam_id", sa.String, nullable=False)
    demo_id = sa.Column("demo_id", sa.String, sa.ForeignKey("demo_metadata.demo_id"), nullable=False)


class Review(Base):
    __tablename__ = "reviews"

    reviewer_steam_id = sa.Column("reviewer_steam_id", sa.String, primary_key=True)
    demo_id = sa.Column("demo_id", sa.String, sa.ForeignKey("demo_metadata.demo_id"), primary_key=True)
    cheat_types = sa.Column("cheat_types", sa.Text, nullable=False)


class DemoMetadata(Base):
    __tablename__ = "demo_metadata"

    demo_id = sa.Column("demo_id", sa.String, primary_key=True)
    file_path = sa.Column("file_path", sa.Text, nullable=False)
    timeseries_data = sa.Column("timeseries_data", JSON)


class PollingSession(Base):
    __tablename__ = "polling_sessions"

    polling_session_id = sa.Column("polling_session_id", sa.String, nullable=False, primary_key=True)
    megabase_user_key = sa.Column("megabase_user_key", sa.String, nullable=False)
    server_steamid64 = sa.Column("server_steamid64", sa.String, nullable=False)
    is_active = sa.Column("is_active", sa.Boolean, nullable=False)
    start_time = sa.Column("start_time", sa.types.TIMESTAMP(timezone=True), nullable=False)
    end_time = sa.Column("end_time", sa.types.TIMESTAMP(timezone=True))
