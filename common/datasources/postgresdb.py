from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

class PostgresDataSource:
    def __init__(self, username, password, host, port, db_name, base=None):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.base = base or declarative_base()
        self.engine = None
        self.session = None

    async def connect(self):
        try:
            database_url = f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            
            self.engine = create_async_engine(
                database_url,
                echo=True,
            )
            self.base.metadata.bind = self.engine  

            self.session = sessionmaker(
                self.engine,
                expire_on_commit=False,
                class_=AsyncSession
            )
            
        except SQLAlchemyError as e:
            self.engine = None
            self.session = None
            raise Exception(f"Database connection error: {e}")

    async def get_session(self):
        if self.engine is None or self.session is None:
            await self.connect()
        return self.session()

    async def close(self):
        if self.engine:
            await self.engine.dispose()
