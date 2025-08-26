# FastAPI CI/CD Demo - Operations Runbook

## 📋 Quick Reference

### 🚀 Emergency Commands
```bash
# Stop all services immediately
make down

# Restart application only
docker-compose restart app

# Check service health
make health

# View real-time logs
make logs

# Restore from backup
make db-restore BACKUP_FILE=backups/backup_YYYYMMDD_HHMMSS.sql
```

### 📞 Contact Information
- **DevOps Team**: devops@company.com
- **On-Call**: +1-555-DEVOPS
- **Incident Response**: #incident-response (Slack)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────┐
│             Load Balancer               │
│              (Nginx)                    │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│           FastAPI App                   │
│         (Docker Container)              │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│          PostgreSQL                     │
│         (Docker Container)              │
└─────────────────────────────────────────┘
```

---

## 🔧 Common Operations

### Daily Operations

#### 1. Health Checks
```bash
# Quick health check
curl http://localhost:8000/healthz

# Detailed service status
make health

# Check all containers
docker-compose ps
```

#### 2. Log Monitoring
```bash
# View all logs
make logs

# Application logs only
make logs-app

# Database logs only
make logs-db

# Follow logs in real-time
docker-compose logs -f app
```

#### 3. Database Maintenance
```bash
# Create backup
make db-backup

# Connect to database
make db-shell

# Check database connections
docker-compose exec db psql -U fastapi -c "SELECT count(*) FROM pg_stat_activity;"
```

### Weekly Operations

#### 1. Security Updates
```bash
# Update dependencies
pip-audit
safety check

# Scan for vulnerabilities
make scan
make scan-docker
```

#### 2. Performance Monitoring
```bash
# Check metrics
curl http://localhost:8000/metrics

# Database performance
docker-compose exec db psql -U fastapi -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

#### 3. Cleanup
```bash
# Clean Docker resources
make clean

# Remove old backups (keep last 7 days)
find backups/ -name "*.sql" -type f -mtime +7 -delete
```

---

## 🚨 Incident Response

### Application Not Responding

#### Symptoms
- Health check returns 503/504
- API endpoints timeout
- Users cannot access the application

#### Diagnosis
```bash
# Check container status
docker-compose ps

# Check application logs
make logs-app

# Check resource usage
docker stats

# Check network connectivity
docker-compose exec app ping db
```

#### Resolution Steps
1. **Restart application container**:
   ```bash
   docker-compose restart app
   ```

2. **If restart fails, rebuild**:
   ```bash
   docker-compose down
   docker-compose up -d --build
   ```

3. **Check database connectivity**:
   ```bash
   docker-compose exec app python -c "from app.db.database import engine; print('DB OK')"
   ```

4. **Rollback if necessary**:
   ```bash
   git checkout <previous-stable-version>
   make deploy-prod
   ```

### Database Issues

#### Symptoms
- Connection refused errors
- Slow query responses
- Database container not running

#### Diagnosis
```bash
# Check database container
docker-compose ps db

# Check database logs
make logs-db

# Check disk space
df -h

# Check database connections
docker-compose exec db psql -U fastapi -c "SELECT count(*) FROM pg_stat_activity;"
```

#### Resolution Steps
1. **Restart database**:
   ```bash
   docker-compose restart db
   ```

2. **Check for long-running queries**:
   ```bash
   docker-compose exec db psql -U fastapi -c "SELECT pid, state, query FROM pg_stat_activity WHERE state = 'active';"
   ```

3. **Restore from backup if corrupted**:
   ```bash
   make db-restore BACKUP_FILE=backups/latest_backup.sql
   ```

### High CPU/Memory Usage

#### Diagnosis
```bash
# Check container resources
docker stats

# Check system resources
top
htop

# Check application metrics
curl http://localhost:8000/metrics | grep process
```

#### Resolution Steps
1. **Identify resource-heavy processes**:
   ```bash
   docker-compose exec app ps aux
   ```

2. **Restart application**:
   ```bash
   docker-compose restart app
   ```

3. **Scale horizontally** (if configured):
   ```bash
   docker-compose up -d --scale app=3
   ```

### Security Incidents

#### Suspicious Activity
1. **Check access logs**:
   ```bash
   make logs | grep -E "(401|403|404)"
   ```

2. **Review recent changes**:
   ```bash
   git log --oneline -10
   ```

3. **Check for unauthorized access**:
   ```bash
   docker-compose exec app grep -E "failed.*login" /var/log/*.log
   ```

4. **Immediate actions**:
   ```bash
   # Rotate JWT secret
   # Update environment variables
   # Restart application
   ```

---

## 🔧 Deployment Operations

### Production Deployment

#### Pre-deployment Checklist
- [ ] Tests pass in CI pipeline
- [ ] Security scans complete
- [ ] Database backup created
- [ ] Maintenance window scheduled
- [ ] Rollback plan ready

#### Deployment Steps
```bash
# 1. Create backup
make db-backup

# 2. Deploy new version
make deploy-prod

# 3. Verify deployment
make health
curl http://production-url/healthz

# 4. Run smoke tests
# Test critical user journeys
```

#### Post-deployment
- [ ] Monitor logs for errors
- [ ] Check metrics dashboard
- [ ] Verify user functionality
- [ ] Update deployment documentation

### Rollback Procedure

#### When to Rollback
- Health checks failing
- Critical functionality broken
- Performance significantly degraded
- Security vulnerability discovered

#### Rollback Steps
```bash
# 1. Identify last known good version
git tag --sort=-version:refname | head -5

# 2. Checkout previous version
git checkout <previous-tag>

# 3. Deploy previous version
make deploy-prod

# 4. Verify rollback
make health

# 5. Restore database if needed
make db-restore BACKUP_FILE=backups/pre_deployment_backup.sql
```

---

## 📊 Monitoring & Alerting

### Key Metrics to Monitor

#### Application Metrics
- Response time (< 200ms target)
- Error rate (< 1% target)
- Request throughput
- Active connections

#### System Metrics
- CPU usage (< 80%)
- Memory usage (< 85%)
- Disk usage (< 90%)
- Network I/O

#### Database Metrics
- Connection count
- Query execution time
- Lock waits
- Cache hit ratio

### Alert Thresholds

#### Critical Alerts
- Application down (health check fails)
- Database down
- Disk space > 95%
- Memory usage > 95%

#### Warning Alerts
- Response time > 500ms
- Error rate > 2%
- CPU usage > 80%
- Disk space > 85%

### Monitoring Commands
```bash
# Application metrics
curl http://localhost:8000/metrics

# System metrics
docker stats --no-stream

# Database metrics
docker-compose exec db psql -U fastapi -c "\l+"
```

---

## 🛠️ Maintenance Tasks

### Daily Tasks
- [ ] Check application logs
- [ ] Verify health checks
- [ ] Monitor resource usage
- [ ] Review error rates

### Weekly Tasks
- [ ] Create database backup
- [ ] Review security logs
- [ ] Update dependencies
- [ ] Clean up old logs/backups

### Monthly Tasks
- [ ] Performance review
- [ ] Security audit
- [ ] Capacity planning
- [ ] Documentation updates

---

## 📝 Configuration Management

### Environment Variables
```bash
# Critical configuration
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=your-secret-key
ENVIRONMENT=production

# Optional configuration
LOG_LEVEL=INFO
ALLOWED_HOSTS=["your-domain.com"]
```

### Configuration Files
- `docker-compose.prod.yml` - Production services
- `.env` - Environment variables
- `alembic.ini` - Database migrations
- `requirements.txt` - Python dependencies

### Secrets Management
- Use GitHub Secrets for CI/CD
- Use environment variables for runtime
- Never commit secrets to git
- Rotate secrets regularly

---

## 🔍 Troubleshooting Guide

### Common Issues

#### "Port already in use" Error
```bash
# Find process using port
sudo lsof -i :8000
sudo netstat -tulpn | grep :8000

# Kill process
sudo kill -9 <PID>

# Or use different port
docker-compose -f docker-compose.yml up -d
```

#### "Database connection refused"
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db
```

#### "Permission denied" Errors
```bash
# Check file permissions
ls -la

# Fix ownership
sudo chown -R $USER:$USER .

# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker
```

#### "Out of disk space"
```bash
# Check disk usage
df -h

# Clean Docker resources
docker system prune -af

# Clean old backups
find backups/ -name "*.sql" -type f -mtime +7 -delete
```

### Performance Issues

#### Slow Response Times
1. Check database query performance
2. Review application logs for bottlenecks
3. Monitor resource usage
4. Consider caching implementation

#### High Memory Usage
1. Check for memory leaks in application
2. Review database connection pooling
3. Monitor garbage collection
4. Consider scaling horizontally

---

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Tools
- **Monitoring**: Prometheus + Grafana
- **Logging**: Structured logging with JSON format
- **Testing**: Pytest + Coverage
- **Security**: Bandit + Safety + Trivy

### Support Channels
- **Internal Wiki**: confluence.company.com/fastapi-cicd
- **Team Chat**: #fastapi-team (Slack)
- **Issue Tracking**: JIRA Project FASTAPI

---

## 📞 Emergency Contacts

### On-Call Rotation
- **Primary**: DevOps Engineer (24/7)
- **Secondary**: Senior Developer
- **Escalation**: Engineering Manager

### Vendor Support
- **Cloud Provider**: support@cloudprovider.com
- **Database**: enterprise@postgresql.org
- **Security**: security@company.com

---

*This runbook is a living document. Please update it when procedures change or new issues are discovered.*

**Last Updated**: December 2023  
**Version**: 1.0  
**Owner**: DevOps Team