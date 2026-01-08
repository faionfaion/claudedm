# Docker Reference

## Dockerfile Best Practices

### Base Image

```dockerfile
FROM python:3.11-bullseye
```

Use specific versions for reproducibility.

### Environment Variables

```dockerfile
ENV PYTHONDONTWRITEBYTECODE 1    # Don't write .pyc files
ENV PYTHONUNBUFFERED 1           # Unbuffered stdout/stderr
ENV DEBIAN_FRONTEND noninteractive  # Non-interactive apt
```

### Layer Optimization

**Combine RUN commands** to reduce layers:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

**Use build arguments for cache busting:**

```dockerfile
ARG REQUIREMENTS_HASH
RUN echo "${REQUIREMENTS_HASH}" > /requirements.hash
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
```

### Multi-stage Builds

```dockerfile
# Build stage
FROM python:3.11 AS builder
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Production stage
FROM python:3.11-slim
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
```

### Security

**Run as non-root:**

```dockerfile
RUN useradd -m -s /bin/bash appuser
USER appuser
```

**Set file permissions:**

```dockerfile
RUN chown -R appuser:appuser /app && \
    chmod -R 755 /app
```

## Docker Commands

### Image Management

```bash
# Build image
docker build -t myapp:latest .

# Build with arguments
docker build --build-arg COMMIT_HASH=$(git rev-parse HEAD) -t myapp:latest .

# List images
docker images

# Remove image
docker rmi myapp:latest

# Remove unused images
docker image prune -a
```

### Container Management

```bash
# Run container
docker run -d --name myapp myapp:latest

# Run with environment variables
docker run -d --name myapp \
  -e DATABASE_URL=postgres://... \
  -e SECRET_KEY=xxx \
  myapp:latest

# Run with port mapping
docker run -d -p 8000:8000 --name myapp myapp:latest

# Run with volume mount
docker run -d -v /host/path:/container/path --name myapp myapp:latest

# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop myapp

# Remove container
docker rm myapp

# Force remove running container
docker rm -f myapp
```

### Logs and Debugging

```bash
# View logs
docker logs myapp

# Follow logs
docker logs -f myapp

# Last N lines
docker logs --tail 50 myapp

# Execute command in container
docker exec -it myapp bash

# Run one-off command
docker exec myapp python manage.py migrate
```

### Image Transfer (tar pattern)

Used when registry is unavailable:

```bash
# Save image to tar
docker save -o myapp.tar myapp:latest

# Transfer to server
scp myapp.tar user@server:~

# Load on server
docker load -i myapp.tar

# Cleanup
rm myapp.tar
```

### Networks

```bash
# List networks
docker network ls

# Create network
docker network create mynetwork

# Inspect network
docker network inspect mynetwork

# Connect container to network
docker network connect mynetwork myapp
```

### Volumes

```bash
# List volumes
docker volume ls

# Create volume
docker volume create myvolume

# Inspect volume
docker volume inspect myvolume

# Remove unused volumes
docker volume prune
```

### Cleanup

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

## Healthchecks

In Dockerfile:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

In docker-compose:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## Common Patterns

### Django Application

```dockerfile
FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Entrypoint Script

```dockerfile
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "main.py"]
```

```bash
#!/bin/bash
set -e

# Run migrations
python manage.py migrate --noinput

# Execute CMD
exec "$@"
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs myapp

# Check container status
docker inspect myapp | jq '.[0].State'

# Run interactively
docker run -it --entrypoint bash myapp:latest
```

### Port already in use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Out of disk space

```bash
# Check Docker disk usage
docker system df

# Cleanup
docker system prune -a --volumes
```

### Container can't reach network

```bash
# Check network settings
docker inspect myapp | jq '.[0].NetworkSettings'

# Test DNS from container
docker exec myapp nslookup google.com
```
