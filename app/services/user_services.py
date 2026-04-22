from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.security import hash_password, verify_password, create_access_token
from app.exceptions.errors import InvalidCredentials


def create_user(db: Session, payload: UserCreate):
    hashed = hash_password(payload.password)
    user = User(
        email=payload.email,
        hashed_password=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials()

    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)

    token = create_access_token({"sub": str(user.id)})

    return token