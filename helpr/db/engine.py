import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv

from pydantic import BaseModel

from .models import *
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession, async_scoped_session
from .models.util import Base



"""#TODO: change name?
class DBConnector():
  
  def __init__(self):
    self.engine = None
    self.sessionmaker = None
  
  async def init(self, drop: bool = False):
    logger.info(f"huhuhuh {self}")
    db_url = os.environ['POSTGRES_URL'].replace('postgresql://', 'postgresql+asyncpg://')
    self.engine = create_async_engine(db_url, echo=False, future=True)
    self.sessionmaker = async_sessionmaker(self.engine, autocommit=False, autoflush=False, expire_on_commit=False)

    if drop:
      print(Base.metadata.tables)
      async with self.sessionmaker() as s:
        await s.execute(text('DROP SCHEMA IF EXISTS public CASCADE'))
        await s.execute(text('CREATE SCHEMA public'))
        await s.commit()
      async with self.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

  async def disconnect(self):
    await self.engine.dispose()

db_connector = DBConnector()

@asynccontextmanager
async def session() -> AsyncGenerator[AsyncSession, None]:
  sessionmaker = async_sessionmaker(self.engine, autocommit=False, autoflush=False, expire_on_commit=False)
  async with db_connector.sessionmaker() as s:
    yield s
    await s.close()

"""
load_dotenv()
db_url = os.environ['POSTGRES_URL'].replace('postgresql://', 'postgresql+asyncpg://')

engine = create_async_engine(db_url, echo=False, future=True)
session = async_scoped_session(async_sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine, expire_on_commit=False), asyncio.current_task)


#TODO: make this secure so it actually cant happen on production
"""async def drop_db():
    print(Base.metadata.tables)
    async with session as s:
      await s.execute(text('DROP SCHEMA IF EXISTS public CASCADE'))
      await s.execute(text('CREATE SCHEMA public'))
      await s.commit()
    async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)
"""