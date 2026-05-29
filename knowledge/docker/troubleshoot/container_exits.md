# Container Exits Immediately

## Problem

The container starts and then stops immediately.

## Common Causes

### Application Crashed

Check logs:

```bash
docker logs container_name
```

### Wrong CMD

Verify Dockerfile:

```dockerfile
CMD ["python", "app.py"]
```

### Missing Environment Variables

Check environment configuration.

### Port Conflicts

Verify mapped ports.

## Investigation Checklist

1. Check logs.
2. Inspect container.
3. Verify CMD.
4. Verify files exist.
5. Run interactively if necessary.

## Useful Command

```bash
docker run -it image_name bash
```

This allows you to debug inside the container.