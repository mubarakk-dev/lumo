# Execute Commands Inside Containers

## Open Bash

```bash
docker exec -it container_name bash
```

---

## Run Single Command

```bash
docker exec container_name ls -la
```

---

## Run As Root

```bash
docker exec -u root container_name whoami
```

---

## Common Use Cases

- Inspect files
- Check logs
- Verify environment variables
- Debug running applications

---

## Common Mistake

Trying to use docker exec on a stopped container.