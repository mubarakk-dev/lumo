# Dockerfile Instructions Cheat Sheet

## FROM

Sets the base image.

```dockerfile
FROM python:3.11-slim
```

---

## WORKDIR

Sets the working directory.

```dockerfile
WORKDIR /app
```

---

## COPY

Copies files into the image.

```dockerfile
COPY . .
```

---

## RUN

Runs commands while building the image.

```dockerfile
RUN pip install -r requirements.txt
```

---

## EXPOSE

Documents which port the container uses.

```dockerfile
EXPOSE 8000
```

---

## ENV

Sets environment variables.

```dockerfile
ENV PYTHON_ENV=production
```

---

## CMD

Defines the default command when the container starts.

```dockerfile
CMD ["python", "app.py"]
```

---

## ENTRYPOINT

Defines a fixed command that runs when the container starts.

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

---

## HEALTHCHECK

Checks whether a container is healthy.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1
```

---

## Related Questions

- Dockerfile commands cheat sheet.
- What does CMD do in Dockerfile?
- Difference between CMD and ENTRYPOINT.
- What is WORKDIR in Docker?
- What does EXPOSE do?