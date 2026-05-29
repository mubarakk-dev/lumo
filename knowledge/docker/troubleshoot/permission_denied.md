# Docker Permission Denied

## Problem

Docker commands fail with permission errors.

---

## Common Error

```text
permission denied while trying to connect to Docker daemon
```

---

## Windows

Verify Docker Desktop is running.

---

## Linux

Add user to docker group:

```bash
sudo usermod -aG docker $USER
```

Log out and back in.

---

## Verify

```bash
docker run hello-world
```

---

## Common Mistake

Running Docker commands before the permission changes take effect.