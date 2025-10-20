## Exercise 0: Docker Hello World 

**Step 1**: Run the Hello World container
```bash
docker run hello-world
```

### Expected Result
You should see a welcome message from Docker explaining what just happened. This is your first successful Docker container run!

## Exercise 0.5: Understanding Docker Concepts
### Task
Learn the fundamental concepts behind Docker before diving deeper.

### What You'll Learn:
- What is a container vs an image?
- How Docker daemon works
- Why containers are useful
- Basic Docker architecture

### Instructions

**Step 1**: Understand images vs containers
```bash
# Images are templates, containers are running instances
docker images                    # See all images
docker run hello-world          # Creates container from image
docker ps -a                    # See all containers (running + stopped)
```

**Step 2**: Explore Docker
```bash
docker version                  # See Docker daemon info
docker info                     # Detailed system information
```

**Step 3**: See the container lifecycle
```bash
# Check what happened to our hello-world container
docker ps -a | grep hello-world
```
### Expected Result
- You understand that images are blueprints and containers are running instances
- You can see Docker system information
- You understand the container lifecycle

## Exercise 1: Run Multiple Containers

### Task
Run three different web servers on different ports and understand port mapping.

### What You'll Learn:
- How to run containers in the background
- Port mapping concepts (host:container)
- Container naming and management
- Different web server images

### Instructions

**Step 1**: Run nginx on port 8080
```bash
docker run -d -p 8080:80 --name web1 nginx:alpine
```
**What this does:**
- `-d`: Run in detached mode (background)
- `-p 8080:80`: Map host port 8080 to container port 80
- `--name web1`: Give the container a friendly name
- `nginx:alpine`: Use the lightweight nginx image

**Step 2**: Run httpd (Apache) on port 8081
```bash
docker run -d -p 8081:80 --name web2 httpd:alpine
```

**Step 3**: Verify both of them are running
```bash
docker ps
```

**Step 4**: Test each server
```bash
curl http://localhost:8080
curl http://localhost:8081
```

**Step 5**: See what images were downloaded
```bash
docker images
```
### Expected Result
You should see three containers running and be able to access all three web servers on different ports.

## Exercise 2: Exploring Container Logs

**Step 1**: Open New Terminal - Generate requests
```bash
# Make requests to web1
for i in {1..5000}; do curl http://localhost:8080; sleep 0.5; done
```

**Step 2**: View the logs
```bash
docker logs web1
```

**Step 3**: Follow logs in real-time (open a new terminal)
```bash
docker logs -f web1
```

**Step 4**: Try different log options
```bash
# Show only last 10 lines
docker logs --tail 10 web1

# Show logs with timestamps
docker logs -t web1
```

### Expected Result
You should see nginx access logs showing GET requests.

### Common Mistakes to Avoid:
- ❌ Not checking logs when containers fail
- ❌ Forgetting that logs are stored even after container stops
- ❌ Not using real-time monitoring for debugging

## Exercise 3: Interactive Container - Using the Shell and Docker Lifecycle


**Step 1**: Run Ubuntu interactively
```bash
docker run -it --name explorer ubuntu bash
```

**What this does:**
- `-i`: Interactive (keep STDIN open)
- `-t`: Allocate a pseudo-TTY (terminal)
- `--name explorer`: Give container a name
- `ubuntu`: Use Ubuntu base image
- `bash`: Run bash shell

**Step 2**: Explore the container
```bash
# Check the OS
cat /etc/os-release

#Check running processes
ps aux

# Create a file
echo "Hello from inside the container!" > test.txt
cat test.txt
```

**Step 3**: Exit the container
```bash
exit
```

**Step 4**: Try to start it again
```bash
docker start explorer
docker exec -it explorer bash
```

**Step 5**: Check if your file is still there
```bash
cat test.txt
```

**Step 6**: Exit the container
```bash
exit
```

**Step 7**: Restart it (stop + start in one command) - 
```bash
docker restart lifecycle
```

**Step 8**: View stats (Ctrl+C to exit) - Resource Monitoring
```bash
docker stats explorer
```

### Bonus: Resource Limits

Run a container with CPU and memory limits:
```bash
docker run -d \
  --name limited \
  --cpus="0.5" \
  --memory="256m" \
  nginx:alpine
```

```bash
# Check the stats
docker stats limited --no-stream
```

### Expected Result
You've practiced start, stop, restart, and remove operations.

### What You Learned:
- [ ] Container lifecycle: create → start → stop → remove
- [ ] Difference between `docker run` (create + start) and `docker start` (start existing)
- [ ] Container states: running, stopped, exited
- [ ] Resource monitoring with `docker stats`
- [ ] Running container with CPU and memory limits



## Exercise 5: Cleanup Challenge (2 minutes)

### Task
Clean up all the containers you created.

### Instructions

**Step 1**: List all containers
```bash
docker ps -a
```

You should see web1, web2, web3, and possibly others.

**Step 2**: Stop all running containers
```bash
docker stop $(docker ps -q)
```

**Step 3**: Remove all containers
```bash
docker rm $(docker ps -aq)
```

Alternative (easier):
```bash
docker container prune
```

**Step 4**: Verify everything is clean
```bash
docker ps -a
```

Should show no containers!

### Expected Result
All containers removed, clean slate.

## Bonus Exercises (If Time Permits)

### Bonus 1: Environment Variables

Run a container with environment variables:
```bash
docker run -d \
  --name env-test \
  -e MY_NAME="Your Name" \
  -e MY_ROLE="Docker Student" \
  -p 8080:80 \
  nginx:alpine

# Execute a command inside the container to see env vars
docker exec env-test env | grep MY_

# Cleanup
docker rm -f env-test
```

### Bonus 2: Resource Limits

Run a container with CPU and memory limits:
```bash
docker run -d \
  --name limited \
  --cpus="0.5" \
  --memory="256m" \
  nginx:alpine

# Check the stats
docker stats limited --no-stream

# Cleanup
docker rm -f limited
```

### Bonus 3: Container Inspection

Inspect a container's detailed configuration:
```bash
docker run -d --name inspect-me nginx:alpine

# View full JSON config
docker inspect inspect-me

# Get just the IP address
docker inspect -f '{{.NetworkSettings.IPAddress}}' inspect-me

# Get just the status
docker inspect -f '{{.State.Status}}' inspect-me

# Cleanup
docker rm -f inspect-me
```

---

## Common Errors & Solutions

### Error: "Conflict. The container name is already in use"
**Solution**: Remove the old container or use a different name
```bash
docker rm container-name
# or
docker rm -f container-name  # Force remove even if running
```

### Error: "Bind for 0.0.0.0:8080 failed: port is already allocated"
**Solution**: Use a different port or stop the conflicting container
```bash
docker run -p 8090:80 nginx  # Use different port
# or
docker ps  # Find what's using 8080
docker stop CONTAINER
```

### Error: "Cannot connect to Docker daemon"
**Solution**: Start Docker
```bash
sudo systemctl start docker  # Linux
# or start Docker Desktop on Mac/Windows
```