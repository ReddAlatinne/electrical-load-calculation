from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import user_services
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse, ErrorResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return user_services.create_user(db, payload)

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=200,
    summary="Authenticate user",
    description="Authenticate a user and return a JWT access token",
    responses={
                401: {"model": ErrorResponse, "description": "Invalid Credentials"}
             }
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    token = user_services.login_user(db, payload.email, payload.password)

    return {
        "access_token": token,
        "token_type": "bearer"
    }