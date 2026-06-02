# Docker Network Types

## Bridge Network

Default Docker network.

Containers can communicate within the same bridge network.

---

## Host Network

Container shares the host network stack.

```bash
docker run --network host nginx
```

---

## None Network

Disables networking.

```bash
docker run --network none nginx
```

---

## Custom Network

```bash
docker network create mynetwork
```

```bash
docker run --network mynetwork nginx
```

---

## Which Should I Use?

Most applications should use:

```text
Bridge Network
```

or

```text
Custom Bridge Network
```

---

## Related Questions

- Docker bridge network.
- Docker host network.
- Docker networking modes.