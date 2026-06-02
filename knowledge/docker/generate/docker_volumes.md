# Create Docker Volumes

## Create Volume

```bash
docker volume create myvolume
```

---

## Use Volume

```bash
docker run -v myvolume:/data nginx
```

---

## List Volumes

```bash
docker volume ls
```

---

## Inspect Volume

```bash
docker volume inspect myvolume
```

---

## Why Use Volumes?

Volumes persist data after containers are removed.

---

## Related Questions

- How do I create a Docker volume?
- Persist Docker data.
- Save data after container restart.