from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

class SQLiteDataSource:
    def __init__(self, db_name, base=None):
        self.db_name = db_name
        self.base = base or declarative_base()
        self.engine = None
        self.SessionLocal = None

    def connect(self):
        try:
            self.engine = create_engine(
                f'sqlite:///{self.db_name}',
                echo=False,  # Disable query logging
            )
            self.base.metadata.create_all(self.engine)  # Ensure tables are created

            self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
            
        except SQLAlchemyError as e:
            self.engine = None
            self.SessionLocal = None
            raise Exception(f"Database connection error: {e}")

    def get_session(self):
        if self.engine is None or self.SessionLocal is None:
            self.connect()
        return self.SessionLocal()

    def close(self):
        if self.engine:
            self.engine.dispose()
