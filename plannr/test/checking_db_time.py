
import os
import os
from contextlib import asynccontextmanager
import time
from typing import AsyncGenerator
from dotenv import load_dotenv

from pydantic import BaseModel



from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
load_dotenv()
start_time = time.time()
db_url = os.environ['POSTGRES_URL'].replace('postgresql://', 'postgresql+asyncpg://')
end_time = time.time()
print(end_time - start_time)
start_time = time.time()
engine = create_async_engine(db_url, echo=False, future=True)

end_time = time.time()
print(end_time - start_time, )
start_time = time.time()
sessionmaker = async_sessionmaker(engine, autocommit=False, autoflush=False, expire_on_commit=False)
end_time = time.time()
print(end_time - start_time, "Huhu")
db_url = os.environ['POSTGRES_URL'].replace('postgresql://', 'postgresql+asyncpg://')
start_time = time.time()
end_time = time.time()
print(end_time - start_time)