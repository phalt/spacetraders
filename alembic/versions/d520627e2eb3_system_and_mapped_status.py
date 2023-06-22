"""system and mapped status

Revision ID: d520627e2eb3
Revises: db75dc8de2cf
Create Date: 2023-06-23 09:51:49.582760

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "d520627e2eb3"
down_revision = "db75dc8de2cf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "systems",
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("sectorSymbol", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("waypoints", sa.JSON(), nullable=False),
        sa.Column("factions", sa.JSON(), nullable=False),
        sa.Column(
            "mapped",
            sa.Enum("UN_MAPPED", "INCOMPLETE", "MAPPED", name="mappedenum"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("symbol"),
    )
    op.create_index(op.f("ix_systems_symbol"), "systems", ["symbol"], unique=False)
    op.add_column(
        "waypoints",
        sa.Column(
            "mapped",
            sa.Enum("UN_MAPPED", "INCOMPLETE", "MAPPED", name="mappedenum"),
            nullable=False,
        ),
    )
    op.create_index(op.f("ix_waypoints_symbol"), "waypoints", ["symbol"], unique=False)
    op.drop_column("waypoints", "visited")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "waypoints",
        sa.Column("visited", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.drop_index(op.f("ix_waypoints_symbol"), table_name="waypoints")
    op.drop_column("waypoints", "mapped")
    op.drop_index(op.f("ix_systems_symbol"), table_name="systems")
    op.drop_table("systems")
    # ### end Alembic commands ###
