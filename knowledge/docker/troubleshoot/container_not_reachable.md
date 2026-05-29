# Container Not Reachable From Browser

## Symptoms

- Application is running
- Container appears healthy
- Browser cannot access the application

---

## Check Port Mapping

Verify:

```bash
docker ps
```

Look for:

```text
0.0.0.0:8080->80/tcp
```

---

## Correct Example

```bash
docker run -p 8080:80 nginx
```

---

## Common Mistakes

### Forgot Port Mapping

Wrong:

```bash
docker run nginx
```

Right:

```bash
docker run -p 8080:80 nginx
```

### Application Listening on Wrong Port

Verify the application port.

### Firewall Restrictions

Check Windows Firewall.

---

## Troubleshooting Checklist

1. Check container running.
2. Check port mapping.
3. Check logs.
4. Verify application port.
5. Test localhost.

## Related Questions

- My Docker app runs but I cannot access it from my browser.
- My container is running but the website does not load.
- Why can't I reach my application?
- Application works inside the container but not from localhost.
- Browser cannot connect to Docker container.
- Container is running but not accessible.