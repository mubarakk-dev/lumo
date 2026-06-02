# Docker Environment Variables

## What Are Environment Variables?

Environment variables allow you to pass configuration into a container without modifying application code.

Examples:

- Database URLs
- API keys
- Application settings
- Environment names

---

## Pass a Variable

```bash
docker run -e APP_ENV=production myapp
```

---

## Multiple Variables

```bash
docker run \
-e APP_ENV=production \
-e DEBUG=false \
myapp
```

---

## Using .env Files

```bash
docker run --env-file .env myapp
```

Example:

```text
APP_ENV=production
DEBUG=false
```

---

## Docker Compose

```yaml
services:
  app:
    environment:
      APP_ENV: production
      DEBUG: false
```

---

## Common Mistakes

- Misspelled variable names
- Missing .env files
- Hardcoding secrets

---

## Related Questions

- How do I pass environment variables?
- How do I use .env files?
- Docker environment variables.
- Docker env example.