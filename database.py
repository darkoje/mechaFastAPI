from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config


class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.open()

    def close(self):
        self.sessionLocal().close()

    def open(self):
        self.engine = create_engine(self.dbname, connect_args={"check_same_thread": False})
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()


database = Database(Config.SQLITE_DB)
