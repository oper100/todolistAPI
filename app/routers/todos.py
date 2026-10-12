from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlmodel import Session, select

from app.database import get_session
from app.models import Todo, TodoCreate, TodoPatch, TodoPut, TodoResponse, User
from app.security import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])


def get_user_todo(todo_id: int, session: Session, user: User) -> Todo:
    todo = session.get(Todo, todo_id)

    if not todo or todo.owner_id != user.id:
        raise HTTPException(
            status_code=404, detail=f"Todo with {todo_id} id not found!"
        )
    return todo


@router.get("/", response_model=list[TodoResponse])
def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return session.exec(
        select(Todo)
        .where(Todo.owner_id == current_user.id)
        .order_by(Todo.id)
        .offset(skip)
        .limit(limit)
    ).all()


@router.post("/", response_model=TodoResponse, status_code=201)
def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    todo = Todo(text=todo_data.text, owner_id=current_user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return get_user_todo(todo_id, session, current_user)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    todo = get_user_todo(todo_id, session, current_user)
    session.delete(todo)
    session.commit()
    return Response(status_code=204)


@router.put("/{todo_id}", response_model=TodoResponse)
def replace_todo(
    todo_id: int,
    todo_data: TodoPut,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    todo = get_user_todo(todo_id, session, current_user)

    todo.text = todo_data.text
    todo.status = todo_data.status

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoPatch,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    todo = get_user_todo(todo_id, session, current_user)
    update_data = todo_data.model_dump(exclude_unset=True, exclude_none=True)
    todo.sqlmodel_update(update_data)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
