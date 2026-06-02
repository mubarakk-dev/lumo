# Environment Variable Issues

## Symptoms

Application behaves incorrectly.

Environment values appear missing.

---

## Verify Variables

```bash
docker exec container_name env
```

---

## Common Causes

- Wrong variable name
- Missing .env file
- Variable not passed to container
- Docker Compose configuration issue

---

## Troubleshooting

1. Check variable names
2. Inspect running container
3. Verify .env file
4. Restart container

---

## Related Questions

- Environment variables not working.
- Docker env missing.
- .env file ignored.