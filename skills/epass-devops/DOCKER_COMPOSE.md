# Docker Compose Reference

## File Structure

Use multiple compose files for different environments:

```
compose-base.yml      # Shared service definitions
compose-develop.yml   # Development overrides
compose-server.yml    # Production overrides
compose-test-ci.yml   # CI testing
```

Run with multiple files:

```bash
docker compose -f compose-base.yml -f compose-server.yml up -d
```

## Version and Services

```yaml
version: "3.9"

services:
  app:
    image: myapp:latest
    container_name: app
```

## Build Configuration

### Simple build:

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
```

### Build with arguments:

```yaml
services:
  app:
    build:
      context: .
      args:
        - COMMIT_HASH=${CI_COMMIT_SHA}
        - REQUIREMENTS_HASH=${REQUIREMENTS_HASH}
```

### External image:

```yaml
services:
  agent:
    image: registry.gitlab.easypay.ua/transport/ai-agent:${AGENT_VERSION:-latest}
```

## Environment Variables

### Direct definition:

```yaml
services:
  app:
    environment:
      - DEBUG=false
      - SECRET_KEY=${SECRET_KEY}
```

### From env file:

```yaml
services:
  app:
    env_file:
      - .env
```

### Variable substitution with defaults:

```yaml
environment:
  - POSTGRES_HOST=${POSTGRES_HOST:-localhost}
  - AGENT_VERSION=${AGENT_VERSION:-latest}
```

## Volumes

### Named volumes (managed by Docker):

```yaml
volumes:
  media: {}
  logs: {}
  static_files: {}

services:
  app:
    volumes:
      - media:/app/media
      - logs:/app/logs
```

### Bind mounts (host directories):

```yaml
services:
  app:
    volumes:
      - ./app:/app
      - /host/path:/container/path
```

### Read-only volumes:

```yaml
volumes:
  - logs:/logs:ro
```

## Networks

### Default network:

All services in same compose file share default network.

### External network:

```yaml
networks:
  epass_default:
    external: true

services:
  app:
    networks:
      - epass_default
```

### Custom network:

```yaml
networks:
  backend:
    driver: bridge

services:
  app:
    networks:
      - backend
```

## Dependencies

### Simple dependency:

```yaml
services:
  app:
    depends_on:
      - db
      - redis
```

### Wait for healthy:

```yaml
services:
  app:
    depends_on:
      db:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
```

## Healthchecks

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s  # Wait before first check
```

Common healthcheck tests:

```yaml
# HTTP check
test: ["CMD", "curl", "-f", "http://localhost:8000/health"]

# TCP check
test: ["CMD", "nc", "-z", "localhost", "5432"]

# Command check
test: ["CMD", "rabbitmqctl", "status"]

# Shell check
test: ["CMD-SHELL", "pg_isready -U postgres"]
```

## Restart Policies

```yaml
services:
  app:
    restart: "always"           # Always restart
    restart: "unless-stopped"   # Restart unless manually stopped
    restart: "on-failure"       # Restart only on failure
    restart: "no"               # Never restart
```

## Logging

```yaml
services:
  rabbitmq:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "10"
```

## Port Mapping

```yaml
services:
  nginx:
    ports:
      - "443:443"       # host:container
      - "8555:8555"

  app:
    expose:
      - "8000"          # Internal only, not exposed to host
```

## YAML Anchors (DRY)

Define reusable configuration:

```yaml
x-app-base: &app-base
  image: myapp:latest
  volumes:
    - media:/media
    - logs:/logs
  env_file:
    - .env

services:
  app:
    <<: *app-base
    container_name: app
    command: ["gunicorn", "config.wsgi"]

  celery:
    <<: *app-base
    container_name: celery
    command: ["celery", "-A", "config", "worker"]

  celery-beat:
    <<: *app-base
    container_name: celery-beat
    command: ["celery", "-A", "config", "beat"]
```

## Commands

### Basic operations:

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Rebuild and start
docker compose up -d --build

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f app
```

### Service management:

```bash
# Restart single service
docker compose restart app

# Stop single service
docker compose stop celery

# Scale service
docker compose up -d --scale worker=3

# Execute command in running container
docker compose exec app python manage.py migrate

# Run one-off command
docker compose run --rm app python manage.py shell
```

### Multiple compose files:

```bash
# Development
docker compose -f compose-base.yml -f compose-develop.yml up -d

# Production
docker compose -f compose-base.yml -f compose-server.yml up -d

# CI testing
docker compose -f compose-test-ci.yml up -d
```

## Environment-Specific Patterns

### Development (compose-develop.yml):

```yaml
services:
  app:
    volumes:
      - ./app:/app  # Mount source for hot reload
    environment:
      - DEBUG=True
    ports:
      - "8000:8000"  # Expose for local access
```

### Production (compose-server.yml):

```yaml
services:
  app:
    restart: "always"
    env_file:
      - .env
    # No source mount, image contains code

  nginx:
    ports:
      - "443:443"
    depends_on:
      - app
```

### CI Testing (compose-test-ci.yml):

```yaml
services:
  postgres-ci:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_pass

  app-ci:
    build:
      context: .
    depends_on:
      - postgres-ci
    environment:
      DATABASE_URL: postgres://test_user:test_pass@postgres-ci/test_db
```

## Troubleshooting

### Container won't start:

```bash
# Check logs
docker compose logs app

# Check container status
docker compose ps

# Run shell in container
docker compose run --rm app bash
```

### Network issues:

```bash
# Inspect network
docker network inspect myproject_default

# Recreate network
docker compose down
docker compose up -d
```

### Volume issues:

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect myproject_media

# Remove unused volumes
docker volume prune
```

### Clean restart:

```bash
# Full cleanup
docker compose down -v --remove-orphans
docker compose up -d --build
```
