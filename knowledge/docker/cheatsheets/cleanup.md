# Docker Cleanup Cheat Sheet

## Show Docker disk usage

```bash
docker system df
```

## Remove unused containers, networks, and images

```bash
docker system prune
```

## Remove unused volumes too

```bash
docker system prune -a --volumes
```

## Remove stopped containers

```bash
docker container prune
```

## Remove unused images

```bash
docker image prune -a
```

## Remove unused volumes

```bash
docker volume prune
```

## Stop all running containers

```bash
docker stop $(docker ps -q)
```

## Remove all containers

```bash
docker rm $(docker ps -aq)
```

## Warning

Be careful with prune commands. They can delete resources you may still need.