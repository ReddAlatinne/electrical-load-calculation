from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import project_services
from app.security import get_current_user
from app.schemas import (
    ProjectCreate,
    BoardOut,
    ProjectOut,
    ErrorResponse
)


router = APIRouter(prefix="/projects", tags=["project"])

@router.post("/",
          response_model=ProjectOut,
          summary="Create new Project",
          description="Create a new project, the server generate an id and create the main board",
          status_code=201,
          responses={
              409: {"model": ErrorResponse, "description": "Existing project name"}
          }

          )
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return project_services.create_project(db, payload, current_user)

