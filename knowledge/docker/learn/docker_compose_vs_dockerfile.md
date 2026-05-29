# Docker Compose vs Dockerfile

## Dockerfile

A Dockerfile describes how to build one Docker image.

It answers:

```text
How should this application image be built?
```

Example instructions:

```dockerfile
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

---

## Docker Compose

Docker Compose describes how multiple services should run together.

It answers:

```text
How should the application stack run?
```

Example services:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"

  db:
    image: postgres:13
```

---

## Key Difference

Dockerfile builds an image.

Docker Compose runs one or more services.

---

## Simple Analogy

Dockerfile = recipe for one dish.

Docker Compose = full dinner plan with multiple dishes.

---

## Related Questions

- Difference between Dockerfile and docker-compose.yml.
- Do I need Dockerfile or Docker Compose?
- What does Docker Compose do?
- What does a Dockerfile do?