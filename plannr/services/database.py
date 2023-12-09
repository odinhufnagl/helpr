from typing import Any, Dict, List, Sequence
from uuid import UUID
from datetime import datetime
from sqlalchemy import update as update_sql
from sqlalchemy.future import select
import db


async def update(model: Any, id: int, data: Dict):
  async with db.session() as session:
    await session.execute(
      update_sql(model)
        .where(model.id == id)
        .values(data)
    )
    await session.commit()

