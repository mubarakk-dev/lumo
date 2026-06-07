# No Space Left On Device

## Problem
Docker fails because the machine or Docker storage area has run out of disk space.

## Cause
Docker can accumulate unused images, stopped containers, build cache, networks, and volumes over time.

## Common Error

```text
no space left on device
```

## Fix

Check Docker disk usage:

```bash
docker system df
```

Remove unused containers, networks, images, and build cache:

```bash
docker system prune
```

Remove unused images and volumes too:

```bash
docker system prune -a --volumes
```

Remove unused volumes only:

```bash
docker volume prune
```

## Warning
Prune commands can delete Docker resources you may still need, especially volumes.
