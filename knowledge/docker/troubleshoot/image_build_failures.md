# Docker Image Build Failures

## Symptoms

- docker build fails
- dependency installation errors
- COPY command errors

---

## Build Command

```bash
docker build -t myapp .
```

---

## Common Causes

### Missing Files

Example:

```dockerfile
COPY requirements.txt .
```

File does not exist.

### Wrong Working Directory

Running build from wrong folder.

### Network Issues

Dependencies cannot be downloaded.

### Dockerfile Syntax Errors

Verify instructions carefully.

---

## Troubleshooting Checklist

1. Read build output.
2. Verify files exist.
3. Verify Dockerfile syntax.
4. Build with:

```bash
docker build --no-cache .
```

## Related Questions

- Why is my docker image failing.