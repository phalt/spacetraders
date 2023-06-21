from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.settings import database_url

DATABASE_URL = database_url()

engine = create_engine(url=DATABASE_URL, pool_size=20, max_overflow=-1)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
