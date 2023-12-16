from fastapi import APIRouter
from pydantic import BaseModel
import db

router = APIRouter(prefix='/admin')

class PostAdminRequest(BaseModel):
    email: str
    password: str


@router.post('')
async def post_admin(request: PostAdminRequest):
    async with db.session() as session:
        db_user = db.models.DBUser(
            email=request.email, password=request.password)
        session.add(db_user)
        await session.flush()
        db_admin = db.models.DBAdmin(user_id=db_user.id)
        session.add(db_admin)
        await session.commit()
    #TODO: should be classes for response
    return "Success"
