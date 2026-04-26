from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from types import SimpleNamespace

from app.models import Project, User, Board
from app.exceptions.errors import ExistingProjectNameError
from app.schemas import (
    ProjectCreate,
)


def create_project(db: Session, payload: ProjectCreate, user: User) -> Project:

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
        simultaneity_factor=1.0,
        is_root=True
    )
    db.add(main_board)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # if known error handle it
        if hasattr(e.orig, "diag") and e.orig.diag.constraint_name == "uq_project_name":
            raise ExistingProjectNameError()
        # else error 500
        raise

    db.refresh(new_project)
    db.refresh(main_board)
    return SimpleNamespace(
        id=new_project.id,
        name=new_project.name,
        created_at=new_project.created_at,
        address=new_project.address,
        status=new_project.status,
        created_board=main_board
    )