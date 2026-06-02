# Docker Compose

Docker Compose is used to manage multi-container applications.

## Start services

```bash
docker-compose up
```

## Start in background

```bash
docker-compose up -d
```

## Build and start

```bash
docker-compose up --build
```

## Stop services

```bash
docker-compose down
```

## Stop and remove volumes

```bash
docker-compose down -v
```

## Example docker-compose.yml

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

## Common Mistake
Changing the Dockerfile but running `docker-compose up` without `--build`.

## Related Questions
- How to build a docker compose?
- Show me an example of Docker Compose.
- Provide an example of Docker Compose.