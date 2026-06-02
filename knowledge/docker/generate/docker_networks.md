# Create Docker Networks

## Create Network

```bash
docker network create mynetwork
```

---

## Run Container On Network

```bash
docker run --network mynetwork nginx
```

---

## List Networks

```bash
docker network ls
```

---

## Inspect Network

```bash
docker network inspect mynetwork
```

---

## Use Case

Allow multiple containers to communicate using container names.

---

## Related Questions

- How do I create a Docker network?
- Containers cannot communicate.
- Docker custom network.