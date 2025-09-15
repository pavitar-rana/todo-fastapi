from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_user, get_db
from starlette import status
from models import Todos


router = APIRouter(prefix="/admin", tags=["admin"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_admin(user: user_dependency, db: db_dependency):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(
    user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(gt=0)]
):
    if not user or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo_model)
    db.commit()
