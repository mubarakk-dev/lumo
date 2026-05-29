# Docker Inspection & Monitoring

## Inspect Container

```bash
docker inspect container_name
```

Shows detailed metadata.

## Get Container Status

```bash
docker inspect --format='{{.State.Status}}' container_name
```

## Get Container IP

```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' container_name
```

## Show Running Processes

```bash
docker top container_name
```

## Monitor Resource Usage

```bash
docker stats
```

## Monitor Docker Events

```bash
docker events
```

## When to Use These Tools

Use inspection tools when:

- a container crashes
- networking behaves strangely
- ports are not working
- CPU or memory usage is high
- debugging deployment issues