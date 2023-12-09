
import asyncio
import os
import sys
from sqlalchemy import select
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload, selectinload
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db

async def main():
    load_dotenv()
    await db.init(True)
   
    async with db.session() as session:

        model = (await session.execute(
            select(db.models.DBClassRoom)
            .where(db.models.DBClassRoom.id == 1)
            .options(selectinload(db.models.DBClassRoom.school))
        )).scalar_one_or_none()

        m = (await session.execute(select(db.models.DBSchool).where(db.models.DBSchool.id == 1).options(selectinload(db.models.DBSchool.class_rooms)))).scalar_one_or_none()
        
        event = db.models.DBTeacherLunchEvent()
        session.add(event)

        await session.commit()

    async with db.session() as session:
        model = (await session.execute(select(db.models.DBClassRoom))).scalars().all()
        await session.commit()

if __name__ == "__main__":
    print(sys.path)
    asyncio.run(main())
