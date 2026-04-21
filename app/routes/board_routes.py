from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import board_services
from app.schemas import (
    BoardCreate,
    BoardOut,
    ErrorResponse
)


router = APIRouter(prefix="/board", tags=["board"])

@router.post("/",
          response_model=BoardOut,
          summary="Create new board",
          description="Create a new board",
          status_code=201,
          responses={
              404: {"model": ErrorResponse, "description": "Project or parent board not found"},
              403: {"model": ErrorResponse, "description": "User not allowed or board not in project"},
              409: {"model": ErrorResponse, "description": "Board name already exists"},
          }
          )
def create_board(payload: BoardCreate, db: Session = Depends(get_db)):
    return board_services.create_board(db, payload)