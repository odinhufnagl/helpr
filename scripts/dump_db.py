import asyncio
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from dotenv import load_dotenv
import sys
from sqlalchemy import select
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../helpr')))

from helpr.db.models.util import Base

from helpr.db.models import DBUser
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession, async_scoped_session

import os


async def main():
    load_dotenv()
    db_url = 'postgresql://postgres:postgres@127.0.0.1:5432/helpr'.replace('postgresql://', 'postgresql+asyncpg://')
    engine = create_async_engine(db_url, echo=True, future=True)
    session = async_scoped_session(async_sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine, expire_on_commit=False), asyncio.current_task)
    async with session() as s:
        await s.execute(text('DROP SCHEMA IF EXISTS public CASCADE'))
        await s.execute(text('CREATE SCHEMA public'))
        await s.commit()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
if __name__ == "__main__":
    print(sys.path)
    asyncio.run(main())
