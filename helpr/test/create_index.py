import sys
import os

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import index
import asyncio
import db
import services.database as db_service
from pathlib import Path
from os.path import abspath
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession, async_scoped_session

import os

relative = Path("docs")
absolute_docs = abspath(relative)  # absolute is a str object


relative2 = Path("index_test")
absolute_location = abspath(relative2)  # absolute is a str object

organization_id = 1
agent_id = 1



os.environ["OPENAI_API_KEY"] = "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"  

async def main():
    db_url = 'postgresql://postgres:postgres@127.0.0.1:5432/helpr'.replace('postgresql://', 'postgresql+asyncpg://')
    engine = create_async_engine(db_url, echo=True, future=True)
    session = async_scoped_session(async_sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine, expire_on_commit=False), asyncio.current_task)
    load_dotenv()
    
    #TODO: a lot to structure here, for example there should be an easy way to create an index and also get it stored and db-created at the same time
    dir_loader = index.DirectoryLoader(directory='docs')
    docs = await dir_loader.load_docs()
    chat_index = index.ChatIndex.construct_default(docs)
    location_to_store = index.IndexLocationDir(dir=absolute_location)
    location_to_store.store_index(chat_index)
    
    async with session() as s:
        db_index = db.models.DBIndex(organization_id=organization_id, location=location_to_store.dir)
        s.add(db_index)
        await s.commit()


if __name__ == "__main__":
    print("starting")
    asyncio.run(main())
    