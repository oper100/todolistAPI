from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.config import settings
from app.database import get_session
from app.models import Token, User, UserCreate, UserResponse
from app.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    user = get_user(user_data.username, session)
    if user:
        raise HTTPException(
            status_code=409,
            detail="Username already taken!",
        )
    hashed_password = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return UserResponse(id=new_user.id, username=new_user.username)
