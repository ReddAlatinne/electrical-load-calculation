from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from jose import jwt, JWTError
from uuid import UUID

from app.config import settings
from app.models import User
from app.schemas import UserCreate
from app.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.exceptions.errors import InvalidCredentials, ExistingEmailError


def create_user(db: Session, payload: UserCreate):
    user = (db.query(User).filter(User.email == payload.email).first())
    if user:
        raise ExistingEmailError()

    hashed = hash_password(payload.password)
    new_user = User(
        email=payload.email,
        hashed_password=hashed,
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # if known error handle it
        if "user_email_key" in str(e.orig):
            raise ExistingEmailError()
        # else error 500
        raise
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials()

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    access_token = create_access_token({
        "sub": str(user.id),
        "type": "access"
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id),
        "type": "refresh"
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def refresh_access_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        token_type = payload.get("type")
        if token_type != "refresh":
            raise InvalidCredentials()

        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidCredentials()

        user_id = UUID(user_id)

    except JWTError:
        raise InvalidCredentials()

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise InvalidCredentials()

    new_access_token = create_access_token({
        "sub": str(user.id),
        "type": "access"
    })

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,  # optional: keep same one
        "token_type": "bearer"
    }