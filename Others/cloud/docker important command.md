## Docker Important Commands

### System Info

```bash
# Show Docker version and info
docker version
docker info

# Show system-wide information
docker system info
```

### Images

```bash
# List all images
docker image ls

# Pull an image from Docker Hub
docker pull <image_name>

# Remove an image
docker rmi <image_name>

# Build an image from a Dockerfile
docker build -t <image_name>:<tag> .

# Tag an image
docker tag <source_image> <target_image>
```

### Containers

```bash
# List running containers
docker ps

docker container ls

# List all containers (including stopped)
docker ps -a

# Run a container interactively
docker run -it <image_name> /bin/bash

# Run a container in detached mode
docker run -d <image_name>

# Stop a running container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Remove all stopped containers
docker container prune

```

### Logs & Exec

```bash
# View logs of a container
docker logs <container_id>

# Follow logs (real-time)
docker logs -f <container_id>

# Execute a command inside a running container
docker exec -it <container_id> /bin/bash
```

### Volumes

```bash
# List volumes
docker volume ls

# Create a volume
docker volume create <volume_name>

# Inspect a volume
docker volume inspect <volume_name>

# Remove a volume
docker volume rm <volume_name>

# Remove all unused volumes
docker volume prune
```

### Networks

```bash
# List networks
docker network ls

# Create a network
docker network create <network_name>

# Inspect a network
docker network inspect <network_name>

# Remove a network
docker network rm <network_name>
```

### Compose

```bash
# Start services defined in docker-compose.yml
docker-compose up

# Start services in detached mode
docker-compose up -d

# Stop services
docker-compose down

# Build or rebuild services
docker-compose build
```

### Clean-Up

```bash
# Remove all stopped containers, unused networks, dangling images, and build cache
docker system prune

# Remove unused images, containers, volumes, and networks
docker system prune -a --volumes
```

### Registry

```bash
# Log in to Docker Hub or other registry
docker login

# Push an image to a registry
docker push <image_name>

# Pull an image from a registry
docker pull <image_name>
```

### Advanced/Debugging

```bash
# Inspect detailed info about containers, images, volumes, or networks
docker inspect <object_id>

# Show container resource usage statistics
docker stats

# Export a container’s filesystem as a tar archive
docker export <container_id> > container.tar

# Import a container filesystem tarball as an image
cat container.tar | docker import - <image_name>

# Save an image as a tar archive
docker save -o <image_name>.tar <image_name>

# Load an image from a tar archive
docker load -i <image_name>.tar
```

---

## Most Frequently Asked in Interviews

- **Basic commands:** `docker run`, `docker ps`, `docker images`, `docker rm`, `docker rmi`
- **Building images:** `docker build -t <name> .`
- **Dockerfile concepts:** layers, caching, CMD vs ENTRYPOINT
- **Volumes:** persistent data storage, `docker volume create`, `-v` flag
- **Networking:** bridge network, exposing ports (`-p`), `docker network create`
- **Docker Compose:** orchestration of multi-container apps, `docker-compose up/down`
- **Cleaning up:** `docker system prune`, removing unused resources
- **Debugging:** `docker logs`, `docker exec`, `docker inspect`
- **Pushing and pulling images:** `docker push`, `docker pull`
- **Container lifecycle:** start, stop, restart, remove containers

These commands and concepts form the foundation for working efficiently with Docker in development and production environments.
