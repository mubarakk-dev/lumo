# Docker Resource Limits

## Limit memory

```bash
docker run --memory=512m nginx
```

## Limit CPU

```bash
docker run --cpus="1.5" nginx
```

## Limit both CPU and memory

```bash
docker run --memory=1g --cpus="2.0" nginx
```

## Restart policy

```bash
docker run --restart=always nginx
```

## What this means

Resource limits control how much CPU and memory a container can use.

## Common mistake

Thinking resource limits change the machine itself. They only limit the container.