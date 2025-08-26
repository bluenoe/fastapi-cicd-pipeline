# FastAPI CI/CD Makefile
# Development automation and deployment commands

.PHONY: help install dev test lint format scan build up down logs clean init-db migrate deploy

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Variables
DOCKER_IMAGE := fastapi-cicd
DOCKER_TAG := latest
COMPOSE_FILE := docker-compose.yml
PROD_COMPOSE_FILE := docker-compose.prod.yml

## Help
help: ## Show this help message
	@echo "$(BLUE)FastAPI CI/CD Makefile$(RESET)"
	@echo "$(BLUE)=====================$(RESET)"
	@echo ""
	@echo "$(GREEN)Available targets:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

## Development
install: ## Install dependencies and setup development environment
	@echo "$(BLUE)Installing dependencies...$(RESET)"
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt
	pre-commit install
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"

dev: ## Start development server with hot reload
	@echo "$(BLUE)Starting development server...$(RESET)"
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload

dev-db: ## Start only the database for development
	@echo "$(BLUE)Starting database...$(RESET)"
	docker-compose up -d db
	@echo "$(GREEN)✓ Database started$(RESET)"

init-db: ## Initialize database with sample data
	@echo "$(BLUE)Initializing database...$(RESET)"
	alembic upgrade head
	python scripts/seed_data.py
	@echo "$(GREEN)✓ Database initialized$(RESET)"

migrate: ## Create new database migration
	@echo "$(BLUE)Creating new migration...$(RESET)"
	@read -p "Migration message: " message; \
	alembic revision --autogenerate -m "$$message"

## Testing
test: ## Run all tests with coverage
	@echo "$(BLUE)Running tests...$(RESET)"
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=70
	@echo "$(GREEN)✓ Tests completed$(RESET)"

test-unit: ## Run only unit tests
	@echo "$(BLUE)Running unit tests...$(RESET)"
	pytest tests/unit/ -v

test-integration: ## Run only integration tests
	@echo "$(BLUE)Running integration tests...$(RESET)"
	pytest tests/integration/ -v

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(RESET)"
	pytest-watch -- tests/ -v

## Code Quality
lint: ## Run linting checks
	@echo "$(BLUE)Running linting checks...$(RESET)"
	black --check .
	ruff check .
	mypy app/ --ignore-missing-imports
	@echo "$(GREEN)✓ Linting completed$(RESET)"

format: ## Format code with black and ruff
	@echo "$(BLUE)Formatting code...$(RESET)"
	black .
	ruff check --fix .
	@echo "$(GREEN)✓ Code formatted$(RESET)"

pre-commit: ## Run pre-commit hooks on all files
	@echo "$(BLUE)Running pre-commit hooks...$(RESET)"
	pre-commit run --all-files

## Security
scan: ## Run security scans
	@echo "$(BLUE)Running security scans...$(RESET)"
	safety check
	bandit -r app/ -ll
	@echo "$(GREEN)✓ Security scan completed$(RESET)"

scan-docker: ## Scan Docker image with Trivy
	@echo "$(BLUE)Scanning Docker image...$(RESET)"
	trivy image $(DOCKER_IMAGE):$(DOCKER_TAG)

## Docker
build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(RESET)"
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .
	@echo "$(GREEN)✓ Docker image built$(RESET)"

build-no-cache: ## Build Docker image without cache
	@echo "$(BLUE)Building Docker image (no cache)...$(RESET)"
	docker build --no-cache -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

up: ## Start all services with docker-compose
	@echo "$(BLUE)Starting all services...$(RESET)"
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)✓ Services started$(RESET)"
	@echo "$(YELLOW)Application: http://localhost:8000$(RESET)"
	@echo "$(YELLOW)API Docs: http://localhost:8000/api/docs$(RESET)"
	@echo "$(YELLOW)Prometheus: http://localhost:9090$(RESET)"
	@echo "$(YELLOW)Grafana: http://localhost:3000$(RESET)"

up-prod: ## Start production services
	@echo "$(BLUE)Starting production services...$(RESET)"
	docker-compose -f $(PROD_COMPOSE_FILE) up -d

down: ## Stop all services
	@echo "$(BLUE)Stopping all services...$(RESET)"
	docker-compose -f $(COMPOSE_FILE) down
	docker-compose -f $(PROD_COMPOSE_FILE) down

logs: ## Show logs from all services
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-app: ## Show logs from app service only
	docker-compose -f $(COMPOSE_FILE) logs -f app

logs-db: ## Show logs from database service only
	docker-compose -f $(COMPOSE_FILE) logs -f db

## Monitoring
monitoring: ## Start monitoring stack (Prometheus + Grafana)
	@echo "$(BLUE)Starting monitoring stack...$(RESET)"
	docker-compose --profile monitoring up -d
	@echo "$(GREEN)✓ Monitoring started$(RESET)"
	@echo "$(YELLOW)Prometheus: http://localhost:9090$(RESET)"
	@echo "$(YELLOW)Grafana: http://localhost:3000 (admin/admin)$(RESET)"

## Database
db-shell: ## Connect to database shell
	docker-compose exec db psql -U fastapi -d fastapi_db

db-backup: ## Create database backup
	@echo "$(BLUE)Creating database backup...$(RESET)"
	mkdir -p backups
	docker-compose exec -T db pg_dump -U fastapi fastapi_db > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Database backup created$(RESET)"

db-restore: ## Restore database from backup (requires BACKUP_FILE variable)
	@echo "$(BLUE)Restoring database...$(RESET)"
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)Error: BACKUP_FILE variable is required$(RESET)"; \
		echo "Usage: make db-restore BACKUP_FILE=backups/backup_20231201_120000.sql"; \
		exit 1; \
	fi
	docker-compose exec -T db psql -U fastapi -d fastapi_db < $(BACKUP_FILE)
	@echo "$(GREEN)✓ Database restored$(RESET)"

## Deployment
deploy-staging: ## Deploy to staging environment
	@echo "$(BLUE)Deploying to staging...$(RESET)"
	# Add staging deployment commands here
	@echo "$(GREEN)✓ Deployed to staging$(RESET)"

deploy-prod: ## Deploy to production environment
	@echo "$(BLUE)Deploying to production...$(RESET)"
	# Add production deployment commands here
	@echo "$(GREEN)✓ Deployed to production$(RESET)"

## Utilities
clean: ## Clean up Docker resources
	@echo "$(BLUE)Cleaning up Docker resources...$(RESET)"
	docker system prune -f
	docker volume prune -f
	@echo "$(GREEN)✓ Cleanup completed$(RESET)"

clean-all: ## Clean up everything (including volumes)
	@echo "$(BLUE)Cleaning up everything...$(RESET)"
	docker-compose -f $(COMPOSE_FILE) down -v
	docker-compose -f $(PROD_COMPOSE_FILE) down -v
	docker system prune -af
	docker volume prune -f
	@echo "$(GREEN)✓ Everything cleaned$(RESET)"

shell: ## Access application container shell
	docker-compose exec app /bin/bash

health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(RESET)"
	@curl -s http://localhost:8000/healthz | jq . || echo "$(RED)App not responding$(RESET)"

setup: install build up init-db ## Complete setup for new developers
	@echo "$(GREEN)✓ Setup completed! Application is ready.$(RESET)"
	@echo "$(YELLOW)Visit http://localhost:8000/api/docs to get started$(RESET)"

## CI/CD simulation
ci: lint test scan ## Run CI pipeline locally
	@echo "$(GREEN)✓ CI pipeline completed successfully$(RESET)"

cd: build scan-docker ## Run CD pipeline locally
	@echo "$(GREEN)✓ CD pipeline completed successfully$(RESET)"