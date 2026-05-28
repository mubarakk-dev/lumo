# What is Docker?

## Definition

Docker is a platform that allows developers to package applications and their dependencies into containers.

A container includes:
- application code
- libraries
- dependencies
- runtime
- configuration

This makes applications portable and consistent across environments.

---

# Analogy

Think of Docker like a shipping container.

No matter what is inside, the container can be transported and run consistently anywhere:
- your laptop
- another developer's machine
- a cloud server

---

# Core Concepts

## Image

An image is a blueprint or template.

It contains:
- operating system layers
- dependencies
- application code

Images are read-only.

Example:
```bash
docker pull nginx
```

---

## Container

A container is a running instance of an image.

You can:
- start it
- stop it
- remove it

Example:
```bash
docker run nginx
```

---

## Dockerfile

A Dockerfile contains instructions for building an image.

Example:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

---

# Why Docker is Useful

## Consistency

Works the same across environments.

## Isolation

Applications run independently.

## Portability

Containers can run almost anywhere.

## Scalability

Easy to deploy multiple containers.

---

# Common Beginner Mistakes

- Confusing images with containers
- Forgetting port mapping
- Running commands from the wrong folder
- Forgetting to rebuild images after code changes

---

# Important Commands

## Pull image
```bash
docker pull nginx
```

## Run container
```bash
docker run nginx
```

## List running containers
```bash
docker ps
```

## Stop container
```bash
docker stop container_name
```

---

# Mental Model

## Image vs Container

Image = recipe

Container = actual meal created from the recipe
