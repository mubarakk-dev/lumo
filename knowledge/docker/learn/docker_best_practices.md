# Docker Best Practices

## Use Small Base Images

Good:

```dockerfile
FROM python:3.11-slim
```

Avoid unnecessarily large images.

---

## Use Specific Tags

Good:

```dockerfile
FROM python:3.11
```

Avoid:

```dockerfile
FROM python:latest
```

---

## Use .dockerignore

Example:

```text
.git
__pycache__
.env
```

---

## Keep Images Small

Remove unnecessary files and dependencies.

---

## Use Multi-Stage Builds

Reduces final image size.

---

## Don't Store Secrets

Never place passwords or API keys directly inside Dockerfiles.

---

## Run as Non-Root

Improves security.

---

## Common Mistake

Building giant images that contain development tools not needed in production.