# Docker Volume Mount Issues

## Symptoms

- Files missing
- Changes not appearing
- Data lost after container restart

---

## Verify Mounts

```bash
docker inspect container_name
```

---

## Example Mount

```bash
docker run -v $(pwd):/app nginx
```

---

## Named Volume

```bash
docker run -v myvolume:/data nginx
```

---

## Common Problems

### Wrong Host Path

Path does not exist.

### Wrong Container Path

Application expects a different directory.

### Permission Issues

Container cannot access mounted files.

---

## Troubleshooting

1. Inspect container.
2. Verify mount path.
3. Check file permissions.
4. Verify data exists.