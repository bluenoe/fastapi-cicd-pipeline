"""
Integration tests for API endpoints.
Tests the complete API flow with database interactions.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user_service import UserService
from app.api.endpoints.auth import get_password_hash


class TestAuthEndpoints:
    """Test cases for authentication endpoints."""
    
    async def test_create_user_and_login(self, client: AsyncClient, db_session: AsyncSession):
        """Test complete user creation and login flow."""
        # Create a new user
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpassword123",
            "is_active": True
        }
        
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["email"] == user_data["email"]
        assert created_user["username"] == user_data["username"]
        assert "id" in created_user
        
        # Login with the created user
        login_data = {
            "username": user_data["username"],
            "password": user_data["password"]
        }
        
        response = await client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        
        return token_data["access_token"]
    
    async def test_login_invalid_credentials(self, client: AsyncClient):
        """Test login with invalid credentials."""
        login_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        
        response = await client.post("/api/v1/auth/token", data=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    async def test_get_current_user(self, client: AsyncClient, db_session: AsyncSession):
        """Test getting current user information."""
        # Create and login user
        token = await self.test_create_user_and_login(client, db_session)
        
        # Get current user info
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == "test@example.com"
        assert user_data["username"] == "testuser"
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401


class TestUserEndpoints:
    """Test cases for user management endpoints."""
    
    async def create_test_user(self, db_session: AsyncSession, is_superuser: bool = False):
        """Helper method to create a test user."""
        user_service = UserService(db_session)
        hashed_password = get_password_hash("testpassword123")
        
        return await user_service.create_user(
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=is_superuser
        )
    
    async def get_auth_token(self, client: AsyncClient, username: str = "testuser"):
        """Helper method to get authentication token."""
        login_data = {
            "username": username,
            "password": "testpassword123"
        }
        
        response = await client.post("/api/v1/auth/token", data=login_data)
        return response.json()["access_token"]
    
    async def test_create_user_success(self, client: AsyncClient):
        """Test successful user creation."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "newpassword123",
            "is_active": True
        }
        
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        
        created_user = response.json()
        assert created_user["email"] == user_data["email"]
        assert created_user["username"] == user_data["username"]
        assert created_user["full_name"] == user_data["full_name"]
        assert created_user["is_active"] == user_data["is_active"]
        assert "id" in created_user
        assert "created_at" in created_user
    
    async def test_create_user_duplicate_email(self, client: AsyncClient, db_session: AsyncSession):
        """Test user creation with duplicate email."""
        # Create first user
        await self.create_test_user(db_session)
        
        # Try to create user with same email
        user_data = {
            "email": "test@example.com",  # Same email
            "username": "differentuser",
            "password": "password123"
        }
        
        response = await client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    async def test_get_user_by_id(self, client: AsyncClient, db_session: AsyncSession):
        """Test getting user by ID."""
        # Create test user
        user = await self.create_test_user(db_session)
        token = await self.get_auth_token(client)
        
        # Get user by ID
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(f"/api/v1/users/{user.id}", headers=headers)
        
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["id"] == user.id
        assert user_data["email"] == user.email
    
    async def test_update_user(self, client: AsyncClient, db_session: AsyncSession):
        """Test updating user information."""
        # Create test user
        user = await self.create_test_user(db_session)
        token = await self.get_auth_token(client)
        
        # Update user
        update_data = {
            "full_name": "Updated Name",
            "email": "updated@example.com"
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.put(f"/api/v1/users/{user.id}", json=update_data, headers=headers)
        
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["full_name"] == update_data["full_name"]
        assert updated_user["email"] == update_data["email"]


class TestPostEndpoints:
    """Test cases for post management endpoints."""
    
    async def create_test_user_and_login(self, client: AsyncClient, db_session: AsyncSession):
        """Helper to create user and get token."""
        user_service = UserService(db_session)
        hashed_password = get_password_hash("testpassword123")
        
        user = await user_service.create_user(
            email="author@example.com",
            username="author",
            full_name="Post Author",
            hashed_password=hashed_password,
            is_active=True
        )
        
        login_data = {
            "username": "author",
            "password": "testpassword123"
        }
        
        response = await client.post("/api/v1/auth/token", data=login_data)
        token = response.json()["access_token"]
        
        return user, token
    
    async def test_create_post(self, client: AsyncClient, db_session: AsyncSession):
        """Test creating a new post."""
        user, token = await self.create_test_user_and_login(client, db_session)
        
        post_data = {
            "title": "Test Post",
            "content": "This is a test post content.",
            "published": True
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post("/api/v1/posts/", json=post_data, headers=headers)
        
        assert response.status_code == 201
        created_post = response.json()
        assert created_post["title"] == post_data["title"]
        assert created_post["content"] == post_data["content"]
        assert created_post["published"] == post_data["published"]
        assert created_post["author_id"] == user.id
    
    async def test_list_posts(self, client: AsyncClient, db_session: AsyncSession):
        """Test listing posts."""
        user, token = await self.create_test_user_and_login(client, db_session)
        
        # Create a few posts
        headers = {"Authorization": f"Bearer {token}"}
        for i in range(3):
            post_data = {
                "title": f"Test Post {i+1}",
                "content": f"Content for post {i+1}",
                "published": True
            }
            await client.post("/api/v1/posts/", json=post_data, headers=headers)
        
        # List posts
        response = await client.get("/api/v1/posts/")
        
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) == 3
        assert all(post["published"] for post in posts)
    
    async def test_get_post_by_id(self, client: AsyncClient, db_session: AsyncSession):
        """Test getting a post by ID."""
        user, token = await self.create_test_user_and_login(client, db_session)
        
        # Create a post
        post_data = {
            "title": "Specific Post",
            "content": "Content for specific post",
            "published": True
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        create_response = await client.post("/api/v1/posts/", json=post_data, headers=headers)
        created_post = create_response.json()
        
        # Get the post
        response = await client.get(f"/api/v1/posts/{created_post['id']}")
        
        assert response.status_code == 200
        post = response.json()
        assert post["id"] == created_post["id"]
        assert post["title"] == post_data["title"]


class TestHealthEndpoints:
    """Test cases for health check endpoints."""
    
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint."""
        response = await client.get("/healthz")
        
        assert response.status_code == 200
        health_data = response.json()
        assert health_data["status"] == "healthy"
        assert "service" in health_data
        assert "version" in health_data
        assert "environment" in health_data
    
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        
        assert response.status_code == 200
        root_data = response.json()
        assert "message" in root_data
        assert "version" in root_data
        assert "docs" in root_data