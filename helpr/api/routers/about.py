
from fastapi import APIRouter

router = APIRouter(prefix='/about')

@router.get('')
def about():
    return "Hello"