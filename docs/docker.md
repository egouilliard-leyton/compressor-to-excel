# Docker Deployment Guide

This guide explains how to build, run, and deploy the Compressor to Excel API using Docker.

## Important: Port Configuration

**Default Ports:**
- **Docker Compose**: Uses port **8001** on the host (mapped to port 8000 in container)
- **Docker Direct**: Uses port **8000** on the host (mapped to port 8000 in container)
- **Local Development**: Uses port **8000**

The container always uses port 8000 internally. Only the host port mapping differs. This allows you to run multiple instances or avoid conflicts with other services.

## Prerequisites

- Docker installed (version 20.10 or later)
- Docker Compose installed (version 2.0 or later, optional but recommended)
- At least 2GB of available disk space
- At least 512MB of available RAM

## Quick Start

### Using Docker Compose (Recommended)

1. **Clone or navigate to the project directory:**
   ```bash
   cd compressor-to-excel
   ```

2. **Copy environment variables template (optional):**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file to customize settings if needed.

3. **Build and start the container:**
   ```bash
   docker-compose up -d
   ```

4. **Check if the API is running:**
   ```bash
   curl http://localhost:8001/api/health
   ```
   
   **Note about ports:**
   - The default host port is **8001** (mapped to container port 8000) to avoid conflicts with other services
   - If port 8001 is in use, you can change it by setting the `PORT` environment variable:
     ```bash
     PORT=8002 docker-compose up -d
     ```
   - The container always uses port 8000 internally; only the host port mapping changes

5. **View logs:**
   ```bash
   docker-compose logs -f api
   ```

6. **Stop the container:**
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build the Docker image:**
   ```bash
   docker build -t compressor-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name compressor-api \
     -p 8000:8000 \
     -e WORKERS=4 \
     -v compressor-temp:/tmp/compressor-api \
     compressor-api
   ```
   Note: You can map to any host port, e.g., `-p 8002:8000` to use port 8002 on the host.

3. **Check if the API is running:**
   ```bash
   # If you mapped to port 8000 on host
   curl http://localhost:8000/api/health
   
   # If you mapped to a different port, use that port instead
   ```

4. **View logs:**
   ```bash
   docker logs -f compressor-api
   ```

5. **Stop the container:**
   ```bash
   docker stop compressor-api
   docker rm compressor-api
   ```

## Configuration

### Environment Variables

The API can be configured using environment variables. See `.env.example` for all available options.

**Key Configuration Options:**

- `HOST`: API host address (default: `0.0.0.0`)
- `PORT`: API port (default: `8000`)
- `WORKERS`: Number of uvicorn workers (default: `4`)
- `MAX_ZIP_SIZE`: Maximum ZIP file size in bytes (default: `524288000` = 500MB)
- `MAX_PDF_SIZE`: Maximum PDF file size in bytes (default: `104857600` = 100MB)
- `MAX_PDFS`: Maximum PDFs per ZIP (default: `100`)
- `PROCESSING_TIMEOUT`: Processing timeout in seconds (default: `3600` = 1 hour)
- `TEMP_DIR`: Temporary directory path (default: `/tmp/compressor-api`)

### Using Environment File

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your desired settings. Docker Compose will automatically load these variables.

### Using Command Line

Pass environment variables directly:

```bash
docker run -d \
  --name compressor-api \
  -p 8000:8000 \
  -e WORKERS=8 \
  -e MAX_ZIP_SIZE=1073741824 \
  compressor-api
```

## Volumes

### Temporary File Storage

The API uses a Docker volume for temporary file storage. This ensures files persist between container restarts and can be managed separately.

**Using Docker Compose:**
The `docker-compose.yml` automatically creates a volume named `compressor-temp`.

**Using Docker directly:**
```bash
docker volume create compressor-temp
docker run -d \
  --name compressor-api \
  -v compressor-temp:/tmp/compressor-api \
  compressor-api
```

### Mounting Host Directory (Development)

For development, you can mount a host directory:

```bash
docker run -d \
  --name compressor-api \
  -p 8000:8000 \
  -v $(pwd)/temp:/tmp/compressor-api \
  compressor-api
```

## Production Deployment

### Resource Limits

The `docker-compose.yml` includes resource limits:
- CPU: Maximum 2 cores, reserved 0.5 cores
- Memory: Maximum 2GB, reserved 512MB

Adjust these in `docker-compose.yml` based on your server capacity.

### Using Gunicorn with Uvicorn Workers

For production, the Dockerfile uses uvicorn with multiple workers. The number of workers can be configured via the `WORKERS` environment variable.

**Recommended worker count:**
- `WORKERS = (2 × CPU cores) + 1`

Example for 4-core server:
```bash
docker run -d \
  --name compressor-api \
  -p 8000:8000 \
  -e WORKERS=9 \
  compressor-api
```

### Health Checks

The container includes a health check that monitors the `/api/health` endpoint. Docker will automatically restart unhealthy containers.

**Check container health:**
```bash
docker ps
# Look for "healthy" status
```

### Logging

View container logs:
```bash
# Using Docker Compose
docker-compose logs -f api

# Using Docker directly
docker logs -f compressor-api
```

### Restart Policy

The `docker-compose.yml` includes `restart: unless-stopped` to ensure the container restarts automatically after system reboots.

## Building Custom Images

### Build with Different Python Version

Edit `Dockerfile` and change the base image:
```dockerfile
FROM python:3.11-slim as builder
```

### Build with Additional Dependencies

Add system packages to the `RUN apt-get install` command in the Dockerfile.

### Tagging Images

```bash
docker build -t compressor-api:latest .
docker build -t compressor-api:v1.0.0 .
docker build -t your-registry/compressor-api:latest .
```

## Troubleshooting

### Container Won't Start

1. **Check logs:**
   ```bash
   docker logs compressor-api
   ```

2. **Check port availability:**
   ```bash
   # Check if port 8001 is available (default Docker Compose port)
   lsof -i :8001 || ss -tuln | grep 8001
   # Or check port 8000 if using Docker directly
   lsof -i :8000 || ss -tuln | grep 8000
   ```
   
   **Port Conflict Resolution:**
   - If port 8001 is in use, you can change it by setting the `PORT` environment variable before running `docker-compose up -d`
   - Example: `PORT=8002 docker-compose up -d`

3. **Check disk space:**
   ```bash
   docker system df
   ```

### API Not Responding

1. **Check if container is running:**
   ```bash
   docker ps
   ```

2. **Check health status:**
   ```bash
   docker inspect compressor-api | grep Health
   ```

3. **Test health endpoint:**
   ```bash
   # For Docker Compose (port 8001 on host)
   curl http://localhost:8001/api/health
   # Or test inside container (port 8000 inside container)
   docker exec compressor-api curl http://localhost:8000/api/health
   ```

### File Upload Issues

1. **Check temporary directory permissions:**
   ```bash
   docker exec compressor-api ls -la /tmp/compressor-api
   ```

2. **Check disk space in volume:**
   ```bash
   docker volume inspect compressor-temp
   ```

3. **Increase file size limits:**
   Set `MAX_ZIP_SIZE` and `MAX_PDF_SIZE` environment variables.

### Performance Issues

1. **Increase worker count:**
   Set `WORKERS` environment variable to match your CPU cores.

2. **Increase resource limits:**
   Update `docker-compose.yml` resource limits.

3. **Monitor resource usage:**
   ```bash
   docker stats compressor-api
   ```

## Updating the Container

### Pull Latest Code

```bash
git pull
docker-compose build --no-cache
docker-compose up -d
```

### Rebuild Without Cache

```bash
docker-compose build --no-cache
docker-compose up -d
```

## Cleaning Up

### Remove Container and Volumes

```bash
# Using Docker Compose
docker-compose down -v

# Using Docker directly
docker stop compressor-api
docker rm compressor-api
docker volume rm compressor-temp
```

### Clean Up Unused Resources

```bash
docker system prune -a
```

## Security Considerations

- The container runs as a non-root user (`appuser`)
- Temporary files are isolated in a Docker volume
- Resource limits prevent resource exhaustion
- Health checks ensure service availability

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

