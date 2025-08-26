"""
User service layer for business logic.
Handles user-related database operations and business rules.
"""

from typing import List, Optional

import structlog
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User

logger = structlog.get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service class for user-related operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination."""
        result = await self.db.execute(
            select(User).offset(skip).limit(limit).order_by(User.created_at.desc())
        )
        return list(result.scalars().all())
    
    async def create_user(
        self,
        email: str,
        username: str,
        hashed_password: str,
        full_name: Optional[str] = None,
        is_active: bool = True,
        is_superuser: bool = False
    ) -> User:
        """Create a new user."""
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
            is_active=is_active,
            is_superuser=is_superuser
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info("User created", user_id=user.id, username=username)
        
        return user
    
    async def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """Update a user's information."""
        user = await self.get_user(user_id)
        if not user:
            return None
        
        for field, value in user_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        await self.db.commit()
        await self.db.refresh(user)
        
        logger.info("User updated", user_id=user_id)
        
        return user
    
    async def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        user = await self.get_user(user_id)
        if not user:
            return False
        
        await self.db.delete(user)
        await self.db.commit()
        
        logger.info("User deleted", user_id=user_id)
        
        return True
    
    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password."""
        user = await self.get_user_by_username(username)
        if not user or not self._verify_password(password, user.hashed_password):
            return None
        return user
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)