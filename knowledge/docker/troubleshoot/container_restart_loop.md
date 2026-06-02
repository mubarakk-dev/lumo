# Container Restart Loop

## Symptoms

Container repeatedly stops and starts.

---

## Check Logs

```bash
docker logs container_name
```

---

## Check Restart Policy

```bash
docker inspect container_name
```

Look for:

```text
RestartPolicy
```

---

## Common Causes

- Application crash
- Missing environment variables
- Database unavailable
- Incorrect startup command

---

## Troubleshooting

1. Check logs
2. Verify startup command
3. Verify dependencies
4. Disable restart policy temporarily

---

## Related Questions

- Container keeps restarting.
- Docker restart loop.
- Container exits then restarts.