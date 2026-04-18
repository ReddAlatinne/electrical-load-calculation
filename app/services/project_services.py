from sqlalchemy.orm import Session
from app.models import Project, User, Board
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

    project = Project(
        owner_id=user.id,
        name=payload.name,
        address=payload.address,
    )
    db.add(project)
    db.flush()

    main_board = Board(
        project_id=project.id,
        name="Main Board",
        simultaneity_factor=1.0
    )
    db.add(main_board)
    db.commit()
    db.refresh(project)
    return {
        "id": project.id,
        "name": project.name,
        "created_at": project.created_at,
        "address": project.address,
        "status": project.status,
        "created_board": main_board
    }