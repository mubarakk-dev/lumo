# Docker Network Connectivity Issues

## Symptoms

- Containers cannot reach each other
- External websites are unreachable
- APIs fail to connect

---

## Check Networks

```bash
docker network ls
```

---

## Inspect Network

```bash
docker network inspect mynetwork
```

---

## Test Connectivity

```bash
docker exec container_name ping google.com
```

---

## Verify Container IP

```bash
docker inspect --format='{{.NetworkSettings.IPAddress}}' container_name
```

---

## Common Causes

- Wrong network configuration
- Missing network attachment
- Firewall restrictions
- DNS issues

---

## Troubleshooting Checklist

1. Check network exists
2. Check container attached
3. Test DNS
4. Test external connectivity
5. Inspect container configuration