# Docker Image Pull Issues

## Common Symptoms

- Image cannot be downloaded
- Authentication error
- Repository not found
- Network timeout

---

## Pull Image

```bash
docker pull nginx
```

---

## Pull Specific Version

```bash
docker pull ubuntu:20.04
```

---

## Login to Docker Hub

```bash
docker login
```

---

## Common Causes

### Wrong Image Name

Check spelling and repository name.

### Missing Login

Private images require authentication.

### Network Issue

Check internet connection.

### Tag Does Not Exist

The requested image version may not exist.

---

## Troubleshooting Checklist

1. Check image name.
2. Check tag.
3. Run `docker login`.
4. Try pulling a known image like `nginx`.
5. Check network connection.

---

## Related Questions

- Docker pull failed.
- Repository not found.
- Cannot pull image from Docker Hub.
- Docker image download failed.
- Authentication required when pulling image.