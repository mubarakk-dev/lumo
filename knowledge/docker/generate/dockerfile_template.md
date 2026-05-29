# Production Dockerfile Template

## Python FastAPI Example

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Explanation

### FROM

Base image.

### WORKDIR

Working directory.

### COPY

Copies files.

### RUN

Installs dependencies.

### EXPOSE

Documents application port.

### CMD

Starts application.