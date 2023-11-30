import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .models import *
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from .models.util import Base

engine: AsyncEngine
sessionmaker: async_sessionmaker


@asynccontextmanager
async def session() -> AsyncGenerator[AsyncSession, None]:
  global sessionmaker
  async with sessionmaker() as s:
    yield s
    await s.close()


async def init(drop: bool = False):
  global engine, sessionmaker
  db_url = os.environ['POSTGRES_URL'].replace('postgresql://', 'postgresql+asyncpg://')
  engine = create_async_engine(db_url, echo=False, future=True)
  sessionmaker = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)

  if drop:
    print(Base.metadata.tables)
    async with sessionmaker() as s:
      await s.execute(text('DROP SCHEMA IF EXISTS public CASCADE'))
      await s.execute(text('CREATE SCHEMA public'))
      await s.commit()
    async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

async def disconnect():
  global engine
  await engine.dispose()
