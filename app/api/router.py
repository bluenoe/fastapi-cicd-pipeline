"""
Main API router that includes all endpoint routers.
Organizes API endpoints in a modular structure.
"""

from fastapi import APIRouter

from app.api.endpoints import auth, posts, users

api_router = APIRouter()

# Include routers with prefixes and tags
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    posts.router,
    prefix="/posts",
    tags=["posts"]
)