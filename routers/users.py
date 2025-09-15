from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user, get_db
from models import Users
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

SECRET_KEY = "HgwXGsGtHxLRQ5HT3yytsci/DV8DoyJSlWABWrFCkLI="
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="user/token")


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_info(
    db: db_dependency,
    user: user_dependency,
):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    return user_model


@router.put("/password", status_code=status.HTTP_200_OK)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    user_verification: Annotated[UserVerification, Body()],
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not user_model:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
