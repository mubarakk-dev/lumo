# What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications.

Instead of running many `docker run` commands manually, you describe your services in a `docker-compose.yml` file.

## Example

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"

  db:
    image: postgres:13
```

## Why it is useful

Docker Compose is useful when an application needs multiple services, such as:

- web app
- database
- cache
- background worker

## Mental Model

Docker Compose is like a project manager for multiple containers.

## Related Questions
- What is Docker Compose?
- Explain Docker Compose.
- What does docker-compose.yml do?
- Why use Docker Compose?