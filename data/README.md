# Sample API Test Data

This directory contains sample data and API testing resources for the FastAPI CI/CD Demo application.

## Contents

### 📄 Postman Collection
- **`postman_collection.json`** - Complete Postman collection with all API endpoints
- **`postman_environment.json`** - Environment variables for Postman testing

### 🧪 Test Data Examples

## Postman Setup Instructions

1. **Import Collection**:
   - Open Postman
   - Click "Import" button
   - Select `postman_collection.json`
   - Click "Import"

2. **Import Environment**:
   - Click on "Environments" in the sidebar
   - Click "Import" button
   - Select `postman_environment.json`
   - Click "Import"

3. **Set Environment**:
   - Select "FastAPI CI/CD - Local Development" from the environment dropdown
   - Ensure your application is running on `http://localhost:8000`

## Quick Test Workflow

1. **Start the application**:
   ```bash
   make up
   make init-db
   ```

2. **Run the complete workflow** in Postman:
   - Go to "Sample Workflow" > "Complete User Workflow"
   - Click "Run" to execute all requests in sequence
   - This will demonstrate the full user journey

## Sample API Requests

### Authentication
```bash
# Login to get access token
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### Create User
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpassword123",
    "is_active": true
  }'
```

### Create Post
```bash
curl -X POST "http://localhost:8000/api/v1/posts/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "title": "My Test Post",
    "content": "This is a test post created via the API.",
    "published": true
  }'
```

### List Posts
```bash
curl -X GET "http://localhost:8000/api/v1/posts/" \
  -H "Accept: application/json"
```

## Sample Data

### Users
The seed data script creates these sample users:

| Username | Email | Password | Role |
|----------|-------|----------|------|
| admin | admin@fastapi-cicd.com | admin123 | Admin |
| johndoe | john.doe@example.com | password123 | User |
| janesmith | jane.smith@example.com | password123 | User |
| bobwilson | bob.wilson@example.com | password123 | User |
| alicejohnson | alice.johnson@example.com | password123 | User |

### Posts
Sample posts are created covering:
- Welcome post explaining the application
- Getting started guide
- DevOps best practices
- Security considerations
- Draft post (unpublished)

## Testing Scenarios

### 1. User Registration & Authentication
- Create new user account
- Login and receive JWT token
- Access protected endpoints

### 2. Content Management
- Create new posts (authenticated)
- List all posts (public)
- Update own posts (authenticated)
- Delete posts (author/admin only)

### 3. Admin Operations
- List all users (admin only)
- Manage user accounts
- Access unpublished content

### 4. Error Handling
- Invalid credentials
- Unauthorized access
- Resource not found
- Validation errors

## Performance Testing

Use the included Postman collection for basic load testing:

1. **Collection Runner**:
   - Select the collection
   - Choose "Run" 
   - Set iterations (e.g., 100)
   - Set delay between requests (e.g., 100ms)

2. **Newman CLI** (for automated testing):
   ```bash
   npm install -g newman
   newman run postman_collection.json -e postman_environment.json
   ```

## API Documentation

When the application is running, visit:
- **Interactive Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Response Examples

### Successful User Creation
```json
{
  "id": 1,
  "email": "testuser@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}
```

### Authentication Token Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Post Creation Response
```json
{
  "id": 1,
  "title": "My Test Post",
  "content": "This is a test post created via the API.",
  "published": true,
  "author_id": 1,
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z"
}
```

### Error Response Example
```json
{
  "detail": "User with this email already exists"
}
```

## Tips for Testing

1. **Use Variables**: Leverage Postman variables for dynamic data
2. **Chain Requests**: Use test scripts to pass data between requests
3. **Validate Responses**: Add assertions in test scripts
4. **Environment Switching**: Use different environments for dev/staging/prod
5. **Documentation**: Keep your API tests documented and organized