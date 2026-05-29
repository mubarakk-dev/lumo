# Docker Registry and Docker Hub

## What is a Registry?

A Docker registry stores Docker images.

The most common registry is Docker Hub.

---

## Login

```bash
docker login
```

---

## Search Images

```bash
docker search nginx
```

---

## Pull an Image

```bash
docker pull nginx
```

---

## Tag an Image

```bash
docker tag myapp:latest username/myapp:v1
```

---

## Push an Image

```bash
docker push username/myapp:v1
```

---

## Typical Workflow

1. Build image
2. Tag image
3. Push image
4. Pull image on another machine

---

## Common Mistakes

- Forgetting to login
- Forgetting to tag before pushing
- Using the wrong repository name