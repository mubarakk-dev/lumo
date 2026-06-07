# Docker Daemon Not Running

## Problem
Docker commands fail because Docker Desktop or the Docker service is not running.

## Cause
Docker Desktop is closed, still starting, or the Docker service has stopped.

## Common Error

```text
Cannot connect to the Docker daemon
```

## Fix on Windows
1. Open Docker Desktop.
2. Wait until it fully starts.
3. Run:

```bash
docker version
```

## Fix on Linux

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

## Verify

```bash
docker run hello-world
```
