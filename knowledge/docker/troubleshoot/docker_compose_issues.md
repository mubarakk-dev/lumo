# Docker Compose Issues

## Common Symptoms

- Services do not start
- Database is not ready
- Containers cannot communicate
- Environment variables are missing
- Changes are not reflected after rebuild

---

## Check Running Services

```bash
docker-compose ps
```

---

## View Logs

```bash
docker-compose logs
docker-compose logs -f
```

---

## Rebuild Services

```bash
docker-compose up --build
```

---

## Stop and Remove Services

```bash
docker-compose down
```

---

## Remove Volumes Too

```bash
docker-compose down -v
```

Use this carefully because it can delete database data.

---

## Common Mistakes

- Forgetting `depends_on`
- Forgetting to rebuild after changing Dockerfile
- Wrong service name
- Wrong environment variable
- Database container not ready yet

---

## Related Questions

- My docker-compose services are not starting.
- Docker Compose database connection failed.
- Why are my Compose changes not showing?
- My services cannot talk to each other in Docker Compose.