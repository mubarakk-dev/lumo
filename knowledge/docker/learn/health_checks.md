# Docker Health Checks

## What Is a Health Check?

A health check allows Docker to determine whether a container is healthy.

---

## Example

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
CMD curl -f http://localhost:8000 || exit 1
```

---

## Inspect Health Status

```bash
docker inspect container_name
```

Look for:

```text
Health
```

---

## Why Use Health Checks?

- Detect unhealthy applications
- Improve reliability
- Support orchestration tools

---

## Common Mistakes

- Health endpoint does not exist
- Timeout too short
- Health check command fails

---

## Related Questions

- How do health checks work?
- Is my container healthy?
- Docker health status.