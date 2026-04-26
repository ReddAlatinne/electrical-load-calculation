from sqlalchemy import (
    Column,
    String,
    Boolean,
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
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    owner = relationship("User", back_populates="projects")
    name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    address = Column(String(250), nullable=True)
    status = Column(String(20), nullable=False, default="active")
    boards = relationship("Board", back_populates="project", cascade="all, delete-orphan")
    __table_args__ = (
        UniqueConstraint('owner_id', 'name', name='uq_project_name'),
    )

    def __repr__(self):
        return f"<Project id={self.id} name={self.name} owner_id={self.owner_id}>"

class Board(Base):
    __tablename__ = "boards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="SET NULL"), nullable=True, index=True)
    simultaneity_factor = Column(Float, default=1.0, nullable=False)
    is_root = Column(Boolean, nullable=False, default=False)
    project = relationship("Project", back_populates="boards")
    parent = relationship("Board", back_populates="children", remote_side=[id])
    children = relationship("Board", back_populates="parent")
    consumers = relationship("Consumer", back_populates="board", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint(
            "simultaneity_factor >= 0 AND simultaneity_factor <= 1",
            name="check_simultaneity_factor_board"
        ),
        UniqueConstraint('project_id', 'name', name='uq_board_name'),
        CheckConstraint(
            "(is_root = TRUE AND parent_id IS NULL) OR (is_root = FALSE)",
            name="check_root_board_consistency"
        ),
    )

    def __repr__(self):
        return f"<Board id={self.id} name={self.name} project_id={self.project_id} parent_id={self.parent_id}>"

class Consumer(Base):
    __tablename__ = "consumers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    board_id = Column(UUID(as_uuid=True), ForeignKey("boards.id", ondelete="CASCADE"), nullable=False, index=True)
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
        CheckConstraint("quantity >= 1", name="check_quantity_positive"),
        CheckConstraint("unit_power_kw >= 0", name="check_power_positive"),
    )

    def __repr__(self):
        return f"<Consumer id={self.id} name={self.name} qty={self.quantity} power={self.unit_power_kw}kW board_id={self.board_id}>"
