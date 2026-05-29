# Multi-Stage Docker Builds

## Why Use Multi-Stage Builds?

Reduces image size.

Separates build dependencies from runtime dependencies.

Improves security.

---

## Example

```dockerfile
FROM node:20 AS builder

WORKDIR /app

COPY . .

RUN npm install

RUN npm run build

FROM nginx:latest

COPY --from=builder /app/dist /usr/share/nginx/html
```

---

## Benefits

- Smaller images
- Faster deployments
- Less attack surface

---

## Common Mistake

Keeping build tools in production images.