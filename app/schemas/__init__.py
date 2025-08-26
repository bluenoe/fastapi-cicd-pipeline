"""
Pydantic schemas for API request/response validation.
Defines the data structures for API endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# User Schemas
class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response data."""
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


# Post Schemas
class PostBase(BaseModel):
    """Base post schema with common fields."""
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None
    published: bool = False


class PostCreate(PostBase):
    """Schema for creating a new post."""
    pass


class PostUpdate(BaseModel):
    """Schema for updating post information."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(PostBase):
    """Schema for post response data."""
    id: int
    author_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""
    username: Optional[str] = None


# Health Check Schema
class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    service: str
    version: str
    environment: str


# Generic Response Schemas
class MessageResponse(BaseModel):
    """Generic message response schema."""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str