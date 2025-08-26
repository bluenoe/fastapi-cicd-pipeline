#!/usr/bin/env python3
"""
Database seeding script.
Creates initial sample data for development and testing.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.database import AsyncSessionLocal
from app.services.user_service import UserService
from app.services.post_service import PostService
from app.api.endpoints.auth import get_password_hash


async def create_sample_users():
    """Create sample users for development."""
    async with AsyncSessionLocal() as session:
        user_service = UserService(session)
        
        # Create admin user
        admin_password = get_password_hash("admin123")
        admin_user = await user_service.create_user(
            email="admin@fastapi-cicd.com",
            username="admin",
            full_name="System Administrator",
            hashed_password=admin_password,
            is_active=True,
            is_superuser=True
        )
        print(f"✓ Created admin user: {admin_user.username}")
        
        # Create regular users
        users_data = [
            {
                "email": "john.doe@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "password123"
            },
            {
                "email": "jane.smith@example.com",
                "username": "janesmith",
                "full_name": "Jane Smith",
                "password": "password123"
            },
            {
                "email": "bob.wilson@example.com",
                "username": "bobwilson",
                "full_name": "Bob Wilson",
                "password": "password123"
            },
            {
                "email": "alice.johnson@example.com",
                "username": "alicejohnson",
                "full_name": "Alice Johnson",
                "password": "password123"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            hashed_password = get_password_hash(user_data["password"])
            user = await user_service.create_user(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password=hashed_password,
                is_active=True
            )
            created_users.append(user)
            print(f"✓ Created user: {user.username}")
        
        return [admin_user] + created_users


async def create_sample_posts(users):
    """Create sample posts for development."""
    async with AsyncSessionLocal() as session:
        post_service = PostService(session)
        
        posts_data = [
            {
                "title": "Welcome to FastAPI CI/CD Demo",
                "content": """
This is a comprehensive FastAPI application demonstrating modern CI/CD practices.

## Features
- FastAPI with async/await
- PostgreSQL with SQLAlchemy ORM
- Alembic database migrations
- Docker containerization
- GitHub Actions CI/CD
- Pre-commit hooks
- Comprehensive testing
- Security best practices
- Monitoring and observability

This post showcases the blog functionality of the application.
                """.strip(),
                "published": True,
                "author_id": users[0].id  # Admin user
            },
            {
                "title": "Getting Started with the API",
                "content": """
To get started with this API, follow these steps:

1. Create a user account using POST /api/v1/users/
2. Login to get an access token using POST /api/v1/auth/token
3. Use the token to access protected endpoints
4. Create and manage your posts

Check out the interactive API documentation at /api/docs for more details.
                """.strip(),
                "published": True,
                "author_id": users[1].id if len(users) > 1 else users[0].id
            },
            {
                "title": "DevOps Best Practices",
                "content": """
This application demonstrates several DevOps best practices:

### CI/CD Pipeline
- Automated testing on every push
- Code quality checks (linting, formatting, type checking)
- Security scanning with Trivy and Bandit
- Automated deployment to staging and production

### Infrastructure as Code
- Docker containers for consistent environments
- Docker Compose for local development
- GitHub Actions for automation

### Monitoring
- Health check endpoints
- Prometheus metrics
- Structured logging
- Error tracking

These practices ensure reliable, secure, and maintainable software delivery.
                """.strip(),
                "published": True,
                "author_id": users[2].id if len(users) > 2 else users[0].id
            },
            {
                "title": "Security Considerations",
                "content": """
Security is a top priority in this application:

### Authentication & Authorization
- JWT tokens for API authentication
- Password hashing with bcrypt
- Role-based access control

### Input Validation
- Pydantic schemas for request validation
- SQL injection prevention with SQLAlchemy
- CORS configuration

### Secrets Management
- Environment variables for sensitive data
- GitHub Secrets for CI/CD
- No hardcoded credentials

### Container Security
- Non-root user in Docker containers
- Minimal base images
- Security scanning in CI pipeline

Regular security audits and updates ensure the application remains secure.
                """.strip(),
                "published": True,
                "author_id": users[3].id if len(users) > 3 else users[0].id
            },
            {
                "title": "Draft: Future Enhancements",
                "content": """
This is a draft post about planned enhancements:

- Rate limiting
- Caching with Redis
- WebSocket support
- Microservices architecture
- Kubernetes deployment
- Advanced monitoring with Grafana dashboards

This post is currently unpublished and only visible to authors and admins.
                """.strip(),
                "published": False,
                "author_id": users[0].id
            }
        ]
        
        for post_data in posts_data:
            post = await post_service.create_post(
                title=post_data["title"],
                content=post_data["content"],
                published=post_data["published"],
                author_id=post_data["author_id"]
            )
            status = "published" if post.published else "draft"
            print(f"✓ Created {status} post: {post.title}")


async def main():
    """Main seeding function."""
    print("🌱 Seeding database with sample data...")
    
    try:
        # Create users
        print("\n👥 Creating sample users...")
        users = await create_sample_users()
        
        # Create posts
        print("\n📝 Creating sample posts...")
        await create_sample_posts(users)
        
        print("\n✅ Database seeding completed successfully!")
        print("\n📋 Sample credentials:")
        print("   Admin: admin / admin123")
        print("   Users: johndoe, janesmith, bobwilson, alicejohnson / password123")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())