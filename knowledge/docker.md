# Docker Cheat Sheet

## What is Docker?
Docker packages an application and everything it needs to run into a container.

## Core Ideas
- **Image**: a blueprint/template.
- **Container**: a running instance of an image.
- **Dockerfile**: instructions for building an image.
- **Docker Compose**: runs multi-container applications.
- **Volume**: persistent storage for containers.
- **Registry**: place to store/share images, such as Docker Hub.

---

# Installation & Setup

## Check Docker version
```bash
docker --version
docker version
docker system info
```

## Test Docker
```bash
docker run hello-world
```

---

# Basic Docker Commands

## Run a container
```bash
docker run nginx
```

## Run interactively
```bash
docker run -it ubuntu:latest bash
```

## Run in background
```bash
docker run -d --name my-container nginx
```

## Run with port mapping
```bash
docker run -p 8080:80 nginx
```

## Auto-remove container after exit
```bash
docker run --rm hello-world
```

---

# Container Management

## List running containers
```bash
docker ps
```

## List all containers
```bash
docker ps -a
```

## Stop a container
```bash
docker stop container_name
```

## Start a stopped container
```bash
docker start container_name
```

## Restart a container
```bash
docker restart container_name
```

## Remove a stopped container
```bash
docker rm container_name
```

## Force remove a running container
```bash
docker rm -f container_name
```

## Remove all stopped containers
```bash
docker container prune
```

---

# Execute Commands Inside Containers

## Open bash inside a running container
```bash
docker exec -it container_name bash
```

## Run a single command
```bash
docker exec container_name ls -la
```

## Run as root
```bash
docker exec -u root container_name whoami
```

---

# Logs & Debugging

## View logs
```bash
docker logs container_name
```

## Follow logs live
```bash
docker logs -f container_name
```

## Show recent logs
```bash
docker logs --tail 50 container_name
```

## Logs with timestamps
```bash
docker logs -t container_name
```

---

# Image Management

## Build image from current folder
```bash
docker build .
```

## Build and tag image
```bash
docker build -t myapp:latest .
```

## Build without cache
```bash
docker build --no-cache -t myapp .
```

## List images
```bash
docker images
```

## Inspect image
```bash
docker inspect image_name
```

## View image history
```bash
docker history image_name
```

## Remove image
```bash
docker rmi image_name
```

## Remove unused images
```bash
docker image prune
```

## Remove all unused images
```bash
docker image prune -a
```

---

# Registry Operations

## Pull image
```bash
docker pull nginx:latest
```

## Pull specific version
```bash
docker pull ubuntu:20.04
```

## Login to Docker Hub
```bash
docker login
```

## Search Docker Hub
```bash
docker search nginx
```

## Tag image
```bash
docker tag myapp:latest username/myapp:v1.0
```

## Push image
```bash
docker push username/myapp:v1.0
```

---

# Dockerfile Basics

## Example Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Common Dockerfile instructions
```dockerfile
FROM ubuntu:20.04
LABEL maintainer="user@example.com"
RUN apt-get update
COPY app.py /app/
WORKDIR /app
EXPOSE 8000
ENV PYTHON_ENV=production
CMD ["python3", "app.py"]
```

---

# Docker Compose

## Start services
```bash
docker-compose up
```

## Start in background
```bash
docker-compose up -d
```

## Build and start
```bash
docker-compose up --build
```

## Stop services
```bash
docker-compose down
```

## Stop and remove volumes
```bash
docker-compose down -v
```

## View services
```bash
docker-compose ps
```

## View logs
```bash
docker-compose logs
docker-compose logs -f
```

## Restart service
```bash
docker-compose restart service_name
```

## Example docker-compose.yml
```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db
    volumes:
      - .:/app

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

---

# Networking

## List networks
```bash
docker network ls
```

## Create network
```bash
docker network create mynetwork
```

## Run container on network
```bash
docker run --network mynetwork nginx
```

## Connect container to network
```bash
docker network connect mynetwork container_name
```

## Inspect network
```bash
docker network inspect mynetwork
```

---

# Port Mapping

## Map port
```bash
docker run -p 8080:80 nginx
```

## Map multiple ports
```bash
docker run -p 8080:80 -p 8443:443 nginx
```

## Map to localhost only
```bash
docker run -p 127.0.0.1:8080:80 nginx
```

---

# Volumes

## Create volume
```bash
docker volume create myvolume
```

## List volumes
```bash
docker volume ls
```

## Inspect volume
```bash
docker volume inspect myvolume
```

## Remove volume
```bash
docker volume rm myvolume
```

## Remove unused volumes
```bash
docker volume prune
```

## Mount named volume
```bash
docker run -v myvolume:/data nginx
```

## Bind mount host folder
```bash
docker run -v /host/path:/container/path nginx
```

## Mount current folder
```bash
docker run -v $(pwd):/app nginx
```

---

# Inspection & Monitoring

## Inspect container
```bash
docker inspect container_name
```

## Get container status
```bash
docker inspect --format='{{.State.Status}}' container_name
```

## Get container IP
```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' container_name
```

## Show processes
```bash
docker top container_name
```

## Show resource usage
```bash
docker stats
```

## Monitor events
```bash
docker events
```

---

# File Operations

## Copy from container to host
```bash
docker cp container_name:/path/to/file ./
```

## Copy from host to container
```bash
docker cp ./file container_name:/path/to/destination
```

---

# Troubleshooting

## Check exit code
```bash
docker inspect --format='{{.State.ExitCode}}' container_name
```

## Check processes
```bash
docker exec container_name ps aux
```

## Test network
```bash
docker exec container_name ping google.com
```

## Check disk usage
```bash
docker exec container_name df -h
```

## Common Docker problems
- Docker daemon is not running.
- Port is already in use.
- Container exits immediately.
- Image was not rebuilt after code changes.
- Command is being run from the wrong folder.
- Volume path is incorrect.
- Environment variables are missing.
- Dockerfile has the wrong working directory.

---

# Cleanup

## Remove unused containers, networks, images
```bash
docker system prune
```

## Remove unused volumes too
```bash
docker system prune -a --volumes
```

## Show disk usage
```bash
docker system df
```

## Stop all running containers
```bash
docker stop $(docker ps -q)
```

## Remove all containers
```bash
docker rm $(docker ps -aq)
```

## Remove all images
```bash
docker rmi $(docker images -q)
```

---

# Resource Limits

## Limit memory
```bash
docker run --memory=512m nginx
```

## Limit CPU
```bash
docker run --cpus="1.5" nginx
```

## Restart policy
```bash
docker run --restart=always nginx
```

---

# Best Practices

## Security
- Do not run containers as root if avoidable.
- Use specific image tags instead of `latest`.
- Scan images for vulnerabilities.
- Keep images small.
- Do not store secrets inside Dockerfiles.

## Dockerfile best practices
- Use `.dockerignore`.
- Use small base images.
- Combine related `RUN` commands.
- Remove package manager cache.
- Use multi-stage builds.
- Expose only required ports.

## Development best practices
- Rebuild after changing Dockerfile.
- Use Compose for multi-container apps.
- Use volumes for local development.
- Check logs before changing random things.
- Keep commands simple first.

---

# Quick Mental Model

## Image vs Container
An image is like a recipe.

A container is like the meal made from that recipe.

## Dockerfile vs docker-compose.yml
A Dockerfile describes how to build one image.

A docker-compose.yml describes how multiple services run together.

## Volume
A volume keeps data even when the container is removed.

## Port mapping
Port mapping connects your laptop to the container.

Example:

```bash
docker run -p 8080:80 nginx
```

Means:

```text
localhost:8080 on your laptop -> port 80 inside container
```
