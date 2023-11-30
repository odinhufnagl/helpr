import asyncio
import os
import sys
from sqlalchemy import select
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db

async def main():
    load_dotenv()
    await db.init(True)
    async with db.session() as session:
      room = db.models.DBClassRoom(name="Odins Klassrum", code="n1")
      session.add(room)
      await session.commit()
      
    async with db.session() as session:
        model = (await session.execute(select(db.models.DBClassRoom))).scalars().all()
        await session.commit()
    
if __name__ == "__main__":
    asyncio.run(main())
   