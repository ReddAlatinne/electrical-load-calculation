from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services import project_services
from app.schemas import (
    ProjectCreate,
    BoardOut,
    ProjectOut
)


router = APIRouter(prefix="/project", tags=["project"])

@router.post("/",
          response_model=ProjectOut,
          summary="Create new Project",
          description="Create a new Project, the server generate an id and the Main Board",
          status_code=201
          )
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    return project_services.create_project(db, payload)