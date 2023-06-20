from sqlalchemy.orm import Session

from src.db import base  # noqa

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from src.db.base import Base  # noqa


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # engine = db.get_bind()
    # Base.metadata.create_all(bind=engine)
    pass
