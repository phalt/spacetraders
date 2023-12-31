"""add waypoint

Revision ID: db75dc8de2cf
Revises: 2a5f7e680d20
Create Date: 2023-06-22 16:05:39.571121

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "db75dc8de2cf"
down_revision = "2a5f7e680d20"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "waypoints",
        sa.Column("systemSymbol", sa.String(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("visited", sa.Boolean(), nullable=True),
        sa.Column("traits", sa.JSON(), nullable=False),
        sa.Column("orbitals", sa.JSON(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("x", sa.Integer(), nullable=False),
        sa.Column("y", sa.Integer(), nullable=False),
        sa.Column("faction", sa.JSON(), nullable=False),
        sa.Column("chart", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("symbol"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("waypoints")
    # ### end Alembic commands ###
