from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Reports(Base):
    __tablename__ = "reports"

    upload_time = sa.Column("upload_time", sa.types.TIMESTAMP(timezone=True), primary_key=True)
    reporter_steam_id = sa.Column("reporter_steam_id", sa.String, primary_key=True)
    suspected_cheater_steam_id = sa.Column("suspected_cheater_steam_id", sa.String, nullable=False)
    demo_id = sa.Column("demo_id", sa.String, sa.ForeignKey("demo_metadata.demo_id"), nullable=False)


class Reviews(Base):
    __tablename__ = "reviews"

    reviewer_steam_id = sa.Column("reviewer_steam_id", sa.String, primary_key=True)
    demo_id = sa.Column("demo_id", sa.String, sa.ForeignKey("demo_metadata.demo_id"), primary_key=True)
    cheat_types = sa.Column("cheat_types", sa.Text, nullable=False)


class DemoMetadata(Base):
    __tablename__ = "demo_metadata"

    demo_id = sa.Column("demo_id", sa.String, primary_key=True)
    file_path = sa.Column("file_path", sa.Text, nullable=False)
    timeseries_data = sa.Column("timeseries_data", JSON)


class PollingSessions(Base):
    __tablename__ = "polling_sessions"

    polling_id = sa.Column("polling_id", sa.String, nullable=False, primary_key=True)
    is_active = sa.Column("is_active", sa.Boolean, nullable=False)
    polling_frequency_ms = sa.Column("polling_frequency_ms", sa.Integer, nullable=False)
    duration_seconds = sa.Column("duration_seconds", sa.String)
