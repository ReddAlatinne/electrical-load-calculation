from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Project, User, Board
from app.exceptions.errors import ExistingProjectNameError
from app.schemas import (
    ProjectCreate
)


def create_project(db: Session, payload: ProjectCreate) -> Project:
    # Until User login is set then remove block
    DEFAULT_EMAIL = "admin@admin.com"
    DEFAULT_ID = "00000000-0000-0000-0000-000000000001"
    user = db.query(User).filter(User.id == DEFAULT_ID).first()
    if not user:
        user = User(
            id=DEFAULT_ID,
            email=DEFAULT_EMAIL
        )
        db.add(user)
        db.flush()
    # Upper Block to remove once user login is set

    project = (db.query(Project).filter(Project.owner_id == user.id,
                       Project.name == payload.name).first())
    if project:
        raise ExistingProjectNameError()

    new_project = Project(
        owner_id=user.id,
        name=payload.name,
        address=payload.address,
    )
    db.add(new_project)
    db.flush()

    main_board = Board(
        project_id=new_project.id,
        name="Main Board",
        simultaneity_factor=1.0
    )
    db.add(main_board)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # if known error handle it
        if "uq_project_name" in str(e.orig):
            raise ExistingProjectNameError()
        # else error 500
        raise

    db.refresh(new_project)
    db.refresh(main_board)
    return {
        "id": new_project.id,
        "name": new_project.name,
        "created_at": new_project.created_at,
        "address": new_project.address,
        "status": new_project.status,
        "created_board": main_board
    }