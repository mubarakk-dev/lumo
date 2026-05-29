# Docker Image Management

## List Images

```bash
docker images
```

## Pull an Image

```bash
docker pull nginx
```

## Pull Specific Version

```bash
docker pull ubuntu:20.04
```

## Remove an Image

```bash
docker rmi image_name
```

## Inspect an Image

```bash
docker inspect image_name
```

## View Image History

```bash
docker history image_name
```

## Tag an Image

```bash
docker tag myapp:latest username/myapp:v1
```

## Push an Image

```bash
docker push username/myapp:v1
```

## Common Mistakes

- Using `latest` everywhere.
- Forgetting to tag before pushing.
- Deleting images still used by containers.