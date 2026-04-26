from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from uuid import UUID

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    address: str | None = Field(default=None, min_length=1, max_length=400)
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "New Project",
                "address": "123 Main Street, New York"
            }
        }
    }

class BoardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_id: UUID = Field(description="Parent board id")
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "New board",
                "parent_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
            }
        }
    }

class BoardOut(BaseModel):
    id: UUID
    name: str
    parent_id: UUID | None = Field(description="Parent board id")
    simultaneity_factor: float
    is_root: bool
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
                "name": "Main Board",
                "parent_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "simultaneity_factor": 1.0,
                "is_root": False
            }
        },
        "from_attributes": True
    }

class ProjectOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    address: str | None
    status: str
    created_board: BoardOut
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "name": "New Project",
                "created_at": "2023-10-27 14:30:05.123456",
                "address": "123 Main Street, New York",
                "status": "active",
                "created_board": {
                    "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12",
                    "name": "Main Board",
                    "parent_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "simultaneity_factor": 1.0,
                    "is_root": True
                }
            }
        },
        "from_attributes": True
    }

class ErrorResponse(BaseModel):
    detail: str

# classes User
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
