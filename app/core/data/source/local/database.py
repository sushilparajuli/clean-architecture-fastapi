from typing import Generator

from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config.env_config import EnvConfig
from app.core.data.source.local.base import Base


class Database:
    def __init__(self, config: EnvConfig):
       # Create database url
       url = URL.create(
           drivername='postgresql+psycopg2',
           username= config.db_user,
           password= config.db_password,
           host= config.db_host,
           port= config.db_port,
           database= config.db_name
       )
       # Create database engine
       self.engine = create_engine(url, echo=True)
       # Create database session
       self.session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
       # Create database base
       self.Base = Base


    def get_session(self) -> Generator[Session, None, None]:
        """
         Create database session
        :return:
            Generator[Session, None, None]: Database session
        """
        db: Session = self.session()
        try:
            yield db
        finally:
            db.close()