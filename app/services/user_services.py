from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import User
from app.schemas import UserCreate
from app.security import hash_password, verify_password, create_access_token
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
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials()

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    token = create_access_token({"sub": str(user.id)})

    return token