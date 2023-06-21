"""create tables~

Revision ID: ee68bbe1c956
Revises:
Create Date: 2023-06-19 19:41:05.442416

"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

from alembic import op

# revision identifiers, used by Alembic.
revision = "ee68bbe1c956"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "demo_metadata",
        sa.Column("demo_id", sa.String(), primary_key=True),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("timeseries_data", JSON),
    )

    op.create_table(
        "reports",
        sa.Column("upload_time", sa.DateTime(timezone=True), primary_key=True),
        sa.Column("reporter_steam_id", sa.String(), primary_key=True),
        sa.Column("suspected_cheater_steam_id", sa.String(), nullable=False),
        sa.Column("demo_id", sa.String(), sa.ForeignKey("demo_metadata.demo_id"), nullable=False),
    )

    op.create_table(
        "reviews",
        sa.Column("reviewer_steam_id", sa.String(), primary_key=True),
        sa.Column("demo_id", sa.String(), sa.ForeignKey("demo_metadata.demo_id"), primary_key=True),
        sa.Column("cheat_types", sa.Text(), nullable=False),
    )

    op.create_table(
        "polling_sessions",
        sa.Column("polling_session_id", sa.String(), nullable=False, primary_key=True),
        sa.Column("megabase_user_key", sa.String(), nullable=False),
        sa.Column("server_steamid64", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("reviews")
    op.drop_table("demo_metadata")
    op.drop_table("polling_sessions")
