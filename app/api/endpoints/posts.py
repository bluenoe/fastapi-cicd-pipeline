"""
Posts management endpoints for CRUD operations.
Handles blog post creation, reading, updating, and deletion.
"""

from typing import Annotated, List

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import get_current_active_user
from app.db.database import get_db_session
from app.models import User
from app.schemas import PostCreate, PostResponse, PostUpdate, MessageResponse
from app.services.post_service import PostService

logger = structlog.get_logger(__name__)

router = APIRouter()


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> PostResponse:
    """Create a new post."""
    post_service = PostService(db)
    
    post = await post_service.create_post(
        title=post_data.title,
        content=post_data.content,
        published=post_data.published,
        author_id=current_user.id
    )
    
    logger.info("New post created", post_id=post.id, author_id=current_user.id)
    
    return PostResponse.model_validate(post)


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    skip: int = 0,
    limit: int = 100,
    published_only: bool = True
) -> List[PostResponse]:
    """List posts with optional filtering."""
    post_service = PostService(db)
    posts = await post_service.get_posts(
        skip=skip, 
        limit=limit, 
        published_only=published_only
    )
    
    return [PostResponse.model_validate(post) for post in posts]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db_session)]
) -> PostResponse:
    """Get a specific post by ID."""
    post_service = PostService(db)
    post = await post_service.get_post(post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    return PostResponse.model_validate(post)


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> PostResponse:
    """Update a post."""
    post_service = PostService(db)
    post = await post_service.get_post(post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Only author or superuser can update
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_post = await post_service.update_post(
        post_id, 
        post_data.model_dump(exclude_unset=True)
    )
    
    logger.info("Post updated", post_id=post_id, updated_by=current_user.username)
    
    return PostResponse.model_validate(updated_post)


@router.delete("/{post_id}", response_model=MessageResponse)
async def delete_post(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> PostResponse:
    """Delete a post."""
    post_service = PostService(db)
    post = await post_service.get_post(post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # Only author or superuser can delete
    if post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    await post_service.delete_post(post_id)
    
    logger.info("Post deleted", post_id=post_id, deleted_by=current_user.username)
    
    return MessageResponse(message="Post deleted successfully")