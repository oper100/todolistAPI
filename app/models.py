from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    status: bool = False
    owner_id: int = Field(foreign_key="user.id", index=True)


class TodoResponse(BaseModel):
    id: int
    text: str
    status: bool


class TodoCreate(SQLModel):
    text: str = Field(min_length=1)


class TodoPut(SQLModel):
    text: str = Field(min_length=1)
    status: bool


class TodoPatch(SQLModel):
    text: str | None = Field(default=None, min_length=1)
    status: bool | None = None


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(SQLModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
