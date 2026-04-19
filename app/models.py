from sqlalchemy import (
    Column,
    String,
    UUID,
    DateTime,
    func,
    ForeignKey,
    Float,
    Integer,
    UniqueConstraint,
    CheckConstraint
)
import uuid
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

class Project(Base):
    __tablename__ = "project"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    address = Column(String(250), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    boards = relationship("Board", back_populates="project", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint('owner_id', 'name', name='uq_project_name'),
    )

class Board(Base):
    __tablename__ = "board"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("board.id"), nullable=True, index=True)
    simultaneity_factor = Column(Float, default=1.0, nullable=False)
    project = relationship("Project", back_populates="boards")
    parent = relationship("Board", back_populates="children", remote_side=[id])
    children = relationship("Board", back_populates="parent")
    consumers = relationship("Consumer", back_populates="board", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint(
            "simultaneity_factor >= 0 AND simultaneity_factor <= 1",
            name="check_simultaneity_factor_board"
        ),
    )

class Consumer(Base):
    __tablename__ = "consumer"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("board.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_power_kw = Column(Float, default=0, nullable=False)
    simultaneity_factor = Column(Float, default=1.0, nullable=False)
    board = relationship("Board", back_populates="consumers")
    __table_args__ = (
        CheckConstraint(
            "simultaneity_factor >= 0 AND simultaneity_factor <= 1",
            name="check_simultaneity_factor_consumer"
        ),
    )
