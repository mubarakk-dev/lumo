# What is a Dockerfile?

A Dockerfile is a text file that contains instructions for building a Docker image.

It tells Docker what base image to use, what files to copy, what dependencies to install, and what command to run.

## Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

CMD ["python", "app.py"]
```

## Why it is useful

A Dockerfile makes your application environment reproducible.

## Mental Model

A Dockerfile is like a recipe for creating a Docker image.

## Related Questions

- What is a Dockerfile?
- Explain Dockerfile.
- What does a Dockerfile do?
- Why use a Dockerfile?