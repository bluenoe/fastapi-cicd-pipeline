"""
Unit tests for user service.
Tests business logic for user operations.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.models import User


class TestUserService:
    """Test cases for UserService class."""
    
    @pytest.fixture
    def mock_db_session(self):
        """Mock database session."""
        return AsyncMock(spec=AsyncSession)
    
    @pytest.fixture
    def user_service(self, mock_db_session):
        """UserService instance with mocked database."""
        return UserService(mock_db_session)
    
    @pytest.fixture
    def sample_user(self):
        """Sample user instance."""
        return User(
            id=1,
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password="$2b$12$hashedpassword",
            is_active=True,
            is_superuser=False
        )
    
    async def test_get_user_success(self, user_service, mock_db_session, sample_user):
        """Test successful user retrieval by ID."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.get_user(1)
        
        # Assert
        assert result == sample_user
        mock_db_session.execute.assert_called_once()
    
    async def test_get_user_not_found(self, user_service, mock_db_session):
        """Test user retrieval when user doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.get_user(999)
        
        # Assert
        assert result is None
        mock_db_session.execute.assert_called_once()
    
    async def test_get_user_by_email_success(self, user_service, mock_db_session, sample_user):
        """Test successful user retrieval by email."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.get_user_by_email("test@example.com")
        
        # Assert
        assert result == sample_user
        mock_db_session.execute.assert_called_once()
    
    async def test_get_user_by_username_success(self, user_service, mock_db_session, sample_user):
        """Test successful user retrieval by username."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.get_user_by_username("testuser")
        
        # Assert
        assert result == sample_user
        mock_db_session.execute.assert_called_once()
    
    async def test_create_user_success(self, user_service, mock_db_session):
        """Test successful user creation."""
        # Arrange
        user_data = {
            "email": "new@example.com",
            "username": "newuser",
            "full_name": "New User",
            "hashed_password": "$2b$12$hashedpassword",
            "is_active": True
        }
        
        # Act
        result = await user_service.create_user(**user_data)
        
        # Assert
        assert result.email == user_data["email"]
        assert result.username == user_data["username"]
        assert result.full_name == user_data["full_name"]
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
    
    async def test_update_user_success(self, user_service, mock_db_session, sample_user):
        """Test successful user update."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        update_data = {"full_name": "Updated Name"}
        
        # Act
        result = await user_service.update_user(1, update_data)
        
        # Assert
        assert result.full_name == "Updated Name"
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
    
    async def test_update_user_not_found(self, user_service, mock_db_session):
        """Test user update when user doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.update_user(999, {"full_name": "New Name"})
        
        # Assert
        assert result is None
        mock_db_session.commit.assert_not_called()
    
    async def test_delete_user_success(self, user_service, mock_db_session, sample_user):
        """Test successful user deletion."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.delete_user(1)
        
        # Assert
        assert result is True
        mock_db_session.delete.assert_called_once_with(sample_user)
        mock_db_session.commit.assert_called_once()
    
    async def test_delete_user_not_found(self, user_service, mock_db_session):
        """Test user deletion when user doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.delete_user(999)
        
        # Assert
        assert result is False
        mock_db_session.delete.assert_not_called()
    
    async def test_authenticate_user_success(self, user_service, mock_db_session, sample_user):
        """Test successful user authentication."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        # Mock password verification
        user_service._verify_password = MagicMock(return_value=True)
        
        # Act
        result = await user_service.authenticate_user("testuser", "password")
        
        # Assert
        assert result == sample_user
        user_service._verify_password.assert_called_once_with("password", sample_user.hashed_password)
    
    async def test_authenticate_user_wrong_password(self, user_service, mock_db_session, sample_user):
        """Test user authentication with wrong password."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_db_session.execute.return_value = mock_result
        
        # Mock password verification to return False
        user_service._verify_password = MagicMock(return_value=False)
        
        # Act
        result = await user_service.authenticate_user("testuser", "wrongpassword")
        
        # Assert
        assert result is None
    
    async def test_authenticate_user_not_found(self, user_service, mock_db_session):
        """Test user authentication when user doesn't exist."""
        # Arrange
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute.return_value = mock_result
        
        # Act
        result = await user_service.authenticate_user("nonexistent", "password")
        
        # Assert
        assert result is None