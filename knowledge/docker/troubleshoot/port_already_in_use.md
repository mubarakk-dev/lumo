# Port Already in Use

## Problem
Docker cannot bind a port because another process is already using it.

## Example Error

```text
port is already allocated
```

## Fix
Use a different host port:

```bash
docker run -p 8081:80 nginx
```

## Explanation
`8081:80` means:

```text
localhost:8081 on your laptop -> port 80 inside the container
```

## Common Mistake
Trying to run two containers on the same host port.
