# Run a Docker Container

## Basic command

```bash
docker run nginx
```

## Run interactively

```bash
docker run -it ubuntu:latest bash
```

## Run in background

```bash
docker run -d --name my-container nginx
```

## Run with port mapping

```bash
docker run -p 8080:80 nginx
```

## Run and auto-remove after exit

```bash
docker run --rm hello-world
```

## Common Mistake
If you are running a web app and cannot access it in the browser, you probably forgot port mapping.
