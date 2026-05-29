# Docker Container Logs

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

## Show logs with timestamps

```bash
docker logs -t container_name
```

## When to use this

Use logs when:
- a container exits immediately
- an app is not responding
- a web server fails to start
- environment variables are missing
- a process crashes

## Common mistake

Changing random Docker commands before checking the logs.