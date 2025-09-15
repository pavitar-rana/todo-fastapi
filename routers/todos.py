from fastapi import Body, APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from db import SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from typing import Annotated
from starlette import status
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Todo backend"}


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(ge=1)]
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/add-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    todo_request: Annotated[TodoRequest, Body()],
    db: db_dependency,
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()
    return {"message": "Todo created successfully"}


@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: Annotated[int, Path(ge=1)],
    todo_request: Annotated[TodoRequest, Body()],
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo_request.title  # type: ignore
    todo_model.description = todo_request.description  # type: ignore
    todo_model.priority = todo_request.priority  # type: ignore
    todo_model.complete = todo_request.complete  # type: ignore

    db.add(todo_model)
    db.commit()
    return {"message": "Todo updated successfully"}


@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: Annotated[int, Path(ge=1)]
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
    return {"message": "Todo deleted successfully"}
