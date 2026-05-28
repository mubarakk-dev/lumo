# Basic Docker Commands

## System information

```bash
docker version
docker system info
docker help
docker <command> --help
```

## Containers

```bash
docker ps
docker ps -a
docker stop container_name
docker start container_name
docker restart container_name
docker rm container_name
```

## Images

```bash
docker images
docker pull nginx
docker build -t myapp:latest .
docker rmi image_name
```

## Logs

```bash
docker logs container_name
docker logs -f container_name
docker logs --tail 50 container_name
```

## Cleanup

```bash
docker system prune
docker image prune
docker container prune
docker volume prune
```
