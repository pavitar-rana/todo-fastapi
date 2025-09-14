from fastapi import Body, APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from db import SessionLocal
from sqlalchemy.orm import Session
from models import Todos
from typing import Annotated
from starlette import status

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Todo backend"}


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: Annotated[int, Path(ge=1)]):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/add-todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: Annotated[TodoRequest, Body()], db: db_dependency):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()
    return {"message": "Todo created successfully"}


@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency,
    todo_id: Annotated[int, Path(ge=1)],
    todo_request: Annotated[TodoRequest, Body()],
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
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
async def delete_todo(db: db_dependency, todo_id: Annotated[int, Path(ge=1)]):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
    return {"message": "Todo deleted successfully"}
