"""
Post service layer for business logic.
Handles post-related database operations and business rules.
"""

from typing import List, Optional

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post

logger = structlog.get_logger(__name__)


class PostService:
    """Service class for post-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_post(self, post_id: int) -> Optional[Post]:
        """Get a post by ID."""
        result = await self.db.execute(select(Post).where(Post.id == post_id))
        return result.scalar_one_or_none()
    
    async def get_posts(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        published_only: bool = True
    ) -> List[Post]:
        """Get a list of posts with pagination and filtering."""
        query = select(Post)
        
        if published_only:
            query = query.where(Post.published == True)
        
        query = query.offset(skip).limit(limit).order_by(Post.created_at.desc())
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def get_posts_by_author(
        self, 
        author_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Post]:
        """Get posts by a specific author."""
        result = await self.db.execute(
            select(Post)
            .where(Post.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .order_by(Post.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def create_post(
        self,
        title: str,
        content: Optional[str] = None,
        published: bool = False,
        author_id: Optional[int] = None
    ) -> Post:
        """Create a new post."""
        post = Post(
            title=title,
            content=content,
            published=published,
            author_id=author_id
        )
        
        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        
        logger.info("Post created", post_id=post.id, title=title)
        
        return post
    
    async def update_post(self, post_id: int, post_data: dict) -> Optional[Post]:
        """Update a post's information."""
        post = await self.get_post(post_id)
        if not post:
            return None
        
        for field, value in post_data.items():
            if hasattr(post, field):
                setattr(post, field, value)
        
        await self.db.commit()
        await self.db.refresh(post)
        
        logger.info("Post updated", post_id=post_id)
        
        return post
    
    async def delete_post(self, post_id: int) -> bool:
        """Delete a post."""
        post = await self.get_post(post_id)
        if not post:
            return False
        
        await self.db.delete(post)
        await self.db.commit()
        
        logger.info("Post deleted", post_id=post_id)
        
        return True
    
    async def publish_post(self, post_id: int) -> Optional[Post]:
        """Publish a post."""
        return await self.update_post(post_id, {"published": True})
    
    async def unpublish_post(self, post_id: int) -> Optional[Post]:
        """Unpublish a post."""
        return await self.update_post(post_id, {"published": False})