# Docker Container Management

## List Running Containers

```bash
docker ps
```

Shows currently running containers.

## List All Containers

```bash
docker ps -a
```

Shows running and stopped containers.

## Stop a Container

```bash
docker stop container_name
```

Example:

```bash
docker stop my-nginx
```

## Start a Container

```bash
docker start container_name
```

## Restart a Container

```bash
docker restart container_name
```

## Remove a Container

```bash
docker rm container_name
```

## Force Remove a Running Container

```bash
docker rm -f container_name
```

## Remove All Stopped Containers

```bash
docker container prune
```

## Common Mistakes

- Removing a container before saving important data.
- Forgetting that `docker rm` only removes containers, not images.
- Confusing `stop` with `remove`.