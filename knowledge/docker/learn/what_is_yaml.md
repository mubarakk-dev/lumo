# What is a YAML File?

YAML is a human-readable configuration format.

In Docker projects, YAML is commonly used for Docker Compose files.

Example:

```yaml
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

The indentation matters because YAML uses spacing to show structure.

## Docker Context

A `docker-compose.yml` file uses YAML to describe services, networks, volumes, ports, and environment variables.

## Common Mistake

YAML is sensitive to indentation. A small spacing mistake can break the file.
