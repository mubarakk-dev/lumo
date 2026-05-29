# Docker Port Mapping

## What is port mapping?

Port mapping connects a port on your laptop to a port inside the container.

## Example

```bash
docker run -p 8080:80 nginx
```

This means:

```text
localhost:8080 on your laptop -> port 80 inside the container
```

## Map multiple ports

```bash
docker run -p 8080:80 -p 8443:443 nginx
```

## Bind to localhost only

```bash
docker run -p 127.0.0.1:8080:80 nginx
```

## Common mistake

Forgetting port mapping and wondering why the app is not available in the browser.