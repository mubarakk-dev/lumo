# Docker Security Basics

## Do Not Store Secrets in Dockerfiles

Avoid putting API keys, passwords, or tokens directly inside a Dockerfile.

Bad:

```dockerfile
ENV API_KEY=my-secret-key
```

---

## Avoid Running as Root

Create a non-root user where possible.

```dockerfile
RUN useradd -m appuser
USER appuser
```

---

## Use Specific Image Tags

Prefer:

```dockerfile
FROM python:3.11-slim
```

Avoid relying on:

```dockerfile
FROM python:latest
```

---

## Keep Images Small

Small images reduce attack surface.

---

## Scan Images

Use image scanning tools where available.

---

## Common Mistakes

- Hardcoding secrets
- Running everything as root
- Using old images
- Using `latest` blindly
- Installing unnecessary packages

---

## Related Questions

- How do I make Docker containers more secure?
- Should Docker containers run as root?
- Is it safe to store secrets in Dockerfile?
- Docker security best practices.