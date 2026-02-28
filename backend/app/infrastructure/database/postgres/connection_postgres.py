import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class ConnectionPostgres:
    def __init__(self):
        self.engine = self.__get_engine()
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=False
        )

    def __get_engine(self):
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL não configurada no .env")

        return create_engine(database_url, pool_pre_ping=True)

    def get_session(self):
        return self.SessionLocal()
