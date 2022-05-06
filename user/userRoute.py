from fastapi import APIRouter
import database, schema
from . import  userModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from . import userService

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

get_db = database.get_db


@router.post('/', response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    return userService.create(request, db)


@router.get('/{id}', response_model=schema.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return userService.show(id, db)