from contextlib import contextmanager
from typing import Generator

from .session import SessionLocal


@contextmanager
def get_db() -> Generator:
    db = SessionLocal()
    yield db
    db.close()
