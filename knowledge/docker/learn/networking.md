# Docker Networking

## What is Docker networking?

Docker networking allows containers to communicate with each other and with your machine.

## List networks

```bash
docker network ls
```

## Create a network

```bash
docker network create mynetwork
```

## Run container on a network

```bash
docker run --network mynetwork nginx
```

## Connect container to network

```bash
docker network connect mynetwork container_name
```

## Inspect network

```bash
docker network inspect mynetwork
```

## Common mistake

Assuming containers can always communicate automatically. In multi-container apps, networking needs to be configured properly.