# FastAPI CI/CD Demo 🚀

[![CI Pipeline](https://github.com/username/fastapi-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/username/fastapi-cicd/actions/workflows/ci.yml)
[![CD Pipeline](https://github.com/username/fastapi-cicd/actions/workflows/cd.yml/badge.svg)](https://github.com/username/fastapi-cicd/actions/workflows/cd.yml)
[![codecov](https://codecov.io/gh/username/fastapi-cicd/branch/main/graph/badge.svg)](https://codecov.io/gh/username/fastapi-cicd)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=username_fastapi-cicd&metric=security_rating)](https://sonarcloud.io/dashboard?id=username_fastapi-cicd)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready FastAPI application demonstrating modern DevOps practices, complete CI/CD pipeline, and industry best practices.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI CI/CD Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐ │
│  │   GitHub        │    │   CI Pipeline   │    │  CD Pipeline    │ │
│  │   Repository    │───▶│   Actions       │───▶│   Deployment    │ │
│  │                 │    │                 │    │                 │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                Application Layer                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │ │
│  │  │   FastAPI   │  │    Auth     │  │    API      │          │ │
│  │  │   Server    │──│   Service   │──│  Endpoints  │          │ │
│  │  │             │  │             │  │             │          │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                  Data Layer                                 │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │ │
│  │  │ PostgreSQL  │  │ SQLAlchemy  │  │  Alembic    │          │ │
│  │  │ Database    │──│    ORM      │──│ Migrations  │          │ │
│  │  │             │  │             │  │             │          │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │              Infrastructure & Monitoring                    │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │ │
│  │  │   Docker    │  │ Prometheus  │  │   Grafana   │          │ │
│  │  │ Containers  │──│  Metrics    │──│ Dashboard   │          │ │
│  │  │             │  │             │  │             │          │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Features

### 🚀 **Application**
- **FastAPI** with async/await support
- **PostgreSQL** database with connection pooling
- **SQLAlchemy** ORM with async support
- **Alembic** database migrations
- **JWT Authentication** with role-based access control
- **Pydantic** data validation and serialization
- **Structured logging** with correlation IDs

### 🔧 **DevOps & CI/CD**
- **Multi-stage Dockerfile** for optimized images
- **Docker Compose** for local development
- **GitHub Actions** CI/CD pipeline
- **Zero-downtime deployments** with health checks
- **Automated testing** with >70% coverage
- **Security scanning** with Trivy and Bandit
- **Pre-commit hooks** for code quality

### 📊 **Observability**
- **Health check endpoints** for load balancers
- **Prometheus metrics** for monitoring
- **Grafana dashboards** for visualization
- **Error tracking** and alerting
- **Performance monitoring**

### 🔒 **Security**
- **Environment-based configuration**
- **Secrets management** via GitHub Actions
- **Container security** best practices
- **SQL injection prevention**
- **CORS configuration**
- **Input validation**

## 🏁 Quick Start

### Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- **Git**

### For Windows Users (WSL2 Setup)

1. **Install WSL2**:
   ```powershell
   # Run in PowerShell as Administrator
   wsl --install
   # Restart your computer
   ```

2. **Install Ubuntu on WSL2**:
   ```powershell
   wsl --install -d Ubuntu
   ```

3. **Setup development environment in WSL2**:
   ```bash
   # Update package list
   sudo apt update && sudo apt upgrade -y
   
   # Install Python and pip
   sudo apt install python3.11 python3.11-venv python3-pip -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo apt install docker-compose -y
   
   # Install make
   sudo apt install make -y
   ```

### For Linux Users

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip docker.io docker-compose make git -y
sudo usermod -aG docker $USER

# CentOS/RHEL
sudo yum install python3.11 python3-pip docker docker-compose make git -y
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/fastapi-cicd.git
   cd fastapi-cicd
   ```

2. **Environment setup**:
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env file with your configuration
   nano .env
   ```

3. **One-command setup** (recommended):
   ```bash
   make setup
   ```

   Or manually:
   ```bash
   # Install dependencies
   make install
   
   # Build and start services
   make build
   make up
   
   # Initialize database
   make init-db
   ```

4. **Access the application**:
   - **API Documentation**: http://localhost:8000/api/docs
   - **Application**: http://localhost:8000
   - **Health Check**: http://localhost:8000/healthz
   - **Metrics**: http://localhost:8000/metrics

## 🛠️ Development

### Available Make Commands

```bash
# Development
make dev                 # Start development server with hot reload
make dev-db             # Start only database for development
make install            # Install dependencies and setup environment
make init-db            # Initialize database with sample data

# Testing
make test               # Run all tests with coverage
make test-unit          # Run only unit tests
make test-integration   # Run only integration tests
make test-watch         # Run tests in watch mode

# Code Quality
make lint               # Run linting checks
make format             # Format code with black and ruff
make pre-commit         # Run pre-commit hooks

# Security
make scan               # Run security scans
make scan-docker        # Scan Docker image with Trivy

# Docker
make build              # Build Docker image
make up                 # Start all services
make down               # Stop all services
make logs               # Show logs from all services

# Database
make db-shell           # Connect to database shell
make db-backup          # Create database backup
make migrate            # Create new database migration

# Utilities
make clean              # Clean up Docker resources
make health             # Check health of all services
```

### 🧪 Testing

Run the complete test suite:

```bash
# Run all tests with coverage
make test

# Run specific test types
make test-unit
make test-integration

# Performance testing
locust -f tests/performance/locustfile.py --host http://localhost:8000
```

### 📊 Monitoring

Start the monitoring stack:

```bash
make monitoring
```

Access monitoring tools:
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

## 🚢 Deployment

### Local Development

```bash
# Start all services
make up

# Check status
make health

# View logs
make logs
```

### Production Deployment

1. **Prepare production environment**:
   ```bash
   # Set production environment variables
   export DOCKER_IMAGE=your-registry/fastapi-cicd
   export IMAGE_TAG=v1.0.0
   export POSTGRES_USER=prod_user
   export POSTGRES_PASSWORD=secure_password
   export SECRET_KEY=your-super-secret-key
   ```

2. **Deploy with zero downtime**:
   ```bash
   make deploy-prod
   ```

### 🔄 CI/CD Pipeline

The project includes comprehensive GitHub Actions workflows:

#### CI Pipeline (`.github/workflows/ci.yml`)
- **Code Quality**: Black, Ruff, MyPy
- **Security**: Safety, Bandit, Semgrep
- **Testing**: Unit, Integration, Coverage
- **Docker**: Build, Trivy scan, Hadolint

#### CD Pipeline (`.github/workflows/cd.yml`)
- **Staging Deployment**: Automatic on main branch
- **Production Deployment**: Manual trigger or tag release
- **Zero-downtime**: Rolling updates with health checks
- **Rollback**: Automated rollback on failure

### Required GitHub Secrets

```bash
# Docker Hub
DOCKER_USERNAME=your-docker-username
DOCKER_PASSWORD=your-docker-password

# Production Server
PRODUCTION_HOST=your-server-ip
PRODUCTION_USER=deploy-user
PRODUCTION_SSH_KEY=your-private-key

# Database
POSTGRES_USER=fastapi
POSTGRES_PASSWORD=secure-password
POSTGRES_DB=fastapi_db

# Application
SECRET_KEY=your-super-secret-key

# Notifications (optional)
SLACK_WEBHOOK_URL=your-slack-webhook
```

## 📁 Project Structure

```
fastapi-cicd/
├── app/                          # Application code
│   ├── api/                      # API routes
│   │   ├── endpoints/            # API endpoints
│   │   └── router.py             # Main router
│   ├── core/                     # Core configuration
│   │   ├── config.py             # Settings
│   │   └── logging.py            # Logging setup
│   ├── db/                       # Database
│   │   └── database.py           # DB connection
│   ├── models/                   # SQLAlchemy models
│   ├── schemas/                  # Pydantic schemas
│   └── services/                 # Business logic
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── performance/              # Performance tests
├── scripts/                      # Utility scripts
├── monitoring/                   # Monitoring config
├── .github/workflows/            # CI/CD pipelines
├── alembic/                      # Database migrations
├── docker-compose.yml            # Development setup
├── docker-compose.prod.yml       # Production setup
├── Dockerfile                    # Multi-stage build
├── Makefile                      # Development commands
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Login and get access token
- `GET /api/v1/auth/me` - Get current user info

### Users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/` - List users (admin only)
- `GET /api/v1/users/{id}` - Get user by ID
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Posts
- `POST /api/v1/posts/` - Create new post
- `GET /api/v1/posts/` - List posts
- `GET /api/v1/posts/{id}` - Get post by ID
- `PUT /api/v1/posts/{id}` - Update post
- `DELETE /api/v1/posts/{id}` - Delete post

### System
- `GET /healthz` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - API information

## 🔒 Security Features

- **JWT Authentication** with configurable expiration
- **Password hashing** using bcrypt
- **SQL injection prevention** via SQLAlchemy ORM
- **Input validation** with Pydantic schemas
- **CORS configuration** for cross-origin requests
- **Environment variables** for sensitive configuration
- **Container security** with non-root user
- **Dependency scanning** in CI pipeline
- **Static code analysis** with multiple tools

## 🌍 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | FastAPI CI/CD Demo |
| `APP_VERSION` | Application version | 1.0.0 |
| `ENVIRONMENT` | Environment (dev/staging/prod) | development |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT secret key | Required |
| `LOG_LEVEL` | Logging level | INFO |
| `LOG_FORMAT` | Log format (json/console) | console |

## 📊 Performance

- **Async/await** for non-blocking operations
- **Connection pooling** for database efficiency
- **Multi-stage Docker builds** for smaller images
- **Health checks** for reliable deployments
- **Monitoring** with Prometheus metrics
- **Load testing** with Locust

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install pre-commit hooks: `pre-commit install`
4. Make your changes and commit: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Create a Pull Request

### Development Workflow

```bash
# Setup development environment
make setup

# Make changes and test
make lint
make test

# Commit changes (pre-commit hooks will run)
git add .
git commit -m "Your commit message"

# Push and create PR
git push origin your-branch
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [Docker](https://www.docker.com/) - Containerization
- [GitHub Actions](https://github.com/features/actions) - CI/CD
- [Prometheus](https://prometheus.io/) - Monitoring

## 📞 Support

- **Documentation**: Check the `/api/docs` endpoint when running
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

---

**Made with ❤️ by Bluenoe**