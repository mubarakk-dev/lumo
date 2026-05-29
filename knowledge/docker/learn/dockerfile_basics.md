# Dockerfile Basics

A Dockerfile is a text file containing instructions for building a Docker image.

## Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

## Common Instructions

### FROM

Defines the base image.

```dockerfile
FROM python:3.11-slim
```

### WORKDIR

Sets the working directory.

```dockerfile
WORKDIR /app
```

### COPY

Copies files into the image.

```dockerfile
COPY . .
```

### RUN

Executes commands during image build.

```dockerfile
RUN pip install -r requirements.txt
```

### EXPOSE

Documents the port used by the application.

```dockerfile
EXPOSE 8000
```

### CMD

Defines the default command when the container starts.

```dockerfile
CMD ["python", "app.py"]
```

## Common Mistakes

- Running COPY before installing dependencies.
- Forgetting WORKDIR.
- Using very large base images.