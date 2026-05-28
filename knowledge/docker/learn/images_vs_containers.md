# Docker Images vs Containers

## Image
A Docker image is a read-only template used to create containers.

Think of an image as a recipe.

Example:

```bash
docker pull nginx
```

This downloads the nginx image.

## Container
A container is a running instance of an image.

Think of a container as the actual meal made from the recipe.

Example:

```bash
docker run nginx
```

## Key Difference
- Image = blueprint
- Container = running thing created from the blueprint

## Useful Commands

List images:

```bash
docker images
```

List running containers:

```bash
docker ps
```

List all containers:

```bash
docker ps -a
```

## Common Mistake
Beginners often think deleting a container deletes the image. It does not.
