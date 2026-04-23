from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Project, User, Board
from app.exceptions.errors import (
    ProjectNotFoundError,
    BoardNotFoundError,
    NotProjectOwnerError,
    NotBoardProjectError,
    ExistingBoardNameError
)
from app.schemas import (
    BoardCreate
)


def create_board(project_id: UUID, db: Session, payload: BoardCreate, user: User) -> Board:
    # Until User login is set then remove block
    """DEFAULT_EMAIL = "admin@admin.com"
    DEFAULT_ID = "00000000-0000-0000-0000-000000000001"
    user = db.query(User).filter(User.id == DEFAULT_ID).first()
    if not user:
        user = User(
            id=DEFAULT_ID,
            email=DEFAULT_EMAIL
        )
        db.add(user)
        db.flush()"""
    # Upper Block to remove once user login is set

    project = (db.query(Project).filter(Project.id == project_id).first())
    parent_board = (db.query(Board).filter(Board.id == payload.parent_id).first())
    '''existing_board = (db.query(Board).filter(Board.project_id == payload.project_id,
                       Board.name == payload.name).first())'''

    if project is None:
        raise ProjectNotFoundError()

    if parent_board is None:
        raise BoardNotFoundError()

    if project.owner_id != user.id:
        raise NotProjectOwnerError()

    if parent_board.project_id != project.id:
        raise NotBoardProjectError()

    '''if existing_board:
        raise ExistingBoardNameError()'''

    new_board = Board(
        project_id=project_id,
        name=payload.name,
        parent_id=payload.parent_id,
    )
    db.add(new_board)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # if known error handle it
        if "uq_board_name" in str(e.orig):
            raise ExistingBoardNameError()
        # else error 500
        raise

    db.refresh(new_board)
    return new_board