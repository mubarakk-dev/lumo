# Copy Files To And From Containers

Use `docker cp` to copy files between your local machine and a container.

## Copy Local File Into A Container

```bash
docker cp ./file.txt container_name:/app/file.txt
```

## Copy Directory Into A Container

```bash
docker cp ./my-folder container_name:/app/my-folder
```

## Copy File From A Container To Local Machine

```bash
docker cp container_name:/app/file.txt ./file.txt
```

## Notes

The container can be running or stopped.

Use `docker ps` to find the container name or ID.
