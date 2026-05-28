# Build a Docker Image

## Command

```bash
docker build -t myapp:latest .
```

## Explanation
- `docker build` builds an image.
- `-t myapp:latest` gives the image a name and tag.
- `.` means use the Dockerfile in the current folder.

## Build without cache

```bash
docker build --no-cache -t myapp:latest .
```

## Common Mistakes
- Running the command from the wrong folder.
- Forgetting to create a Dockerfile.
- Forgetting to rebuild after changing dependencies.
