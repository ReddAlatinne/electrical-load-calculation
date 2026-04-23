from fastapi import APIRouter, Query, Depends
from sqlalchemy import Uuid
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import get_db
from app.security import get_current_user
from app.services import board_services
from app.schemas import (
    BoardCreate,
    BoardOut,
    ErrorResponse
)


router = APIRouter(tags=["board"])

@router.post("/projects/{project_id}/boards",
          response_model=BoardOut,
          summary="Create new board",
          description="Create a new board under the specified parent board within a project",
          status_code=201,
          responses={
              404: {"model": ErrorResponse, "description": "Project or parent board not found"},
              403: {"model": ErrorResponse, "description": "User not allowed or board not in project"},
              409: {"model": ErrorResponse, "description": "Board name already exists"},
          }
          )
def create_board(project_id: UUID, payload: BoardCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return board_services.create_board(project_id, db, payload, current_user)