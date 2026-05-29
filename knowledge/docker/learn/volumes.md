# Docker Volumes

## What is a volume?

A Docker volume is persistent storage for containers.

Containers are temporary, but volumes allow data to survive even if a container is removed.

## Create a volume

```bash
docker volume create myvolume
```

## List volumes

```bash
docker volume ls
```

## Inspect a volume

```bash
docker volume inspect myvolume
```

## Remove a volume

```bash
docker volume rm myvolume
```

## Mount a named volume

```bash
docker run -v myvolume:/data nginx
```

## Mount current folder

```bash
docker run -v $(pwd):/app nginx
```

## Common mistake

Thinking container data is always permanent. Without volumes, important data can disappear when the container is removed.