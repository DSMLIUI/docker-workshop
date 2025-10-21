# Docker Workshop for Data Science & Machine Learning

> A comprehensive hands-on workshop covering Docker fundamentals through deploying AI/ML applications to the cloud.

## 🎯 Workshop Overview

This workshop takes you from Docker basics to deploying a tiny LLM (Large Language Model) application in the cloud. Through practical exercises, you'll learn containerization concepts essential for modern data science and machine learning workflows.

## 📚 Workshop Modules

### Module 1: Docker Basics
**Duration:** ~1 hour  
**Difficulty:** Beginner

Learn the fundamentals of Docker containers and images.

**What You'll Learn:**
- Docker architecture and concepts
- Running containers from existing images
- Container lifecycle management (start, stop, restart)
- Port mapping and networking basics
- Working with container logs
- Interactive containers and shell access
- Resource monitoring and limits
- Environment variables
- Container cleanup and management

**Key Exercises:**
- Run your first Docker container (Hello World)
- Run multiple web servers on different ports
- Explore container logs in real-time
- Work with interactive Ubuntu containers
- Monitor resource usage with `docker stats`
- Clean up containers and images

---

### Module 2: Building Docker Images
**Duration:** ~1.5 hours  
**Difficulty:** Intermediate

Master the art of creating custom Docker images and learn Dockerfile best practices.

**What You'll Learn:**
- Dockerfile syntax and structure
- Building custom images from scratch
- Layer caching optimization
- Multi-stage builds (if applicable)
- Best practices for AI/ML workloads
- Security considerations (non-root users)
- Health checks for production
- Handling large dependencies (PyTorch, Transformers)

**Key Exercises:**
- Create your first Dockerfile
- Build a Story Generator TinyLLM application
- Optimize Dockerfile for layer caching
- Work with large ML dependencies
- Implement security best practices

**Featured Project:**
- **Story Generator TinyLLM App**
  - Uses DistilGPT2 (80MB lightweight LLM)
  - Streamlit chat interface
  - Optimized for 512MB RAM
  - Production-ready Dockerfile with health checks

---

### Module 3: Docker Compose
**Duration:** ~1 hour  
**Difficulty:** Intermediate

Learn to orchestrate multi-container applications with Docker Compose.

**What You'll Learn:**
- Why Docker Compose is needed
- YAML configuration syntax
- Service orchestration
- Docker networking between containers
- Volume management for data persistence
- Environment variable management
- Service dependencies and health checks
- Database initialization scripts
- Troubleshooting multi-container apps

**Key Exercises:**
- Set up a PostgreSQL + pgAdmin stack
- Configure Docker networks for service communication
- Persist data with Docker volumes
- Connect services using service names
- Test data persistence across container restarts
- Debug service communication issues

**Featured Project:**
- **E-Commerce Database Demo**
  - PostgreSQL database with sample data
  - pgAdmin web interface for database management
  - Automatic initialization with sample data
  - Data persistence with volumes

---

### Module 4: Deploy TinyLLM to Cloud
**Duration:** ~1 hour  
**Difficulty:** Intermediate to Advanced

Deploy your containerized LLM application to the cloud.

**What You'll Learn:**
- Cloud deployment pipeline
- Docker registries (Docker Hub)
- Image tagging strategies
- Pushing images to registries
- Cloud platform deployment (OnRender)
- Production considerations
- Getting a public HTTPS URL
- Sharing your application globally

**Key Exercises:**
- Create a Docker Hub account
- Tag and push images to Docker Hub
- Set up OnRender cloud platform
- Deploy from Docker Hub to cloud
- Access your live application via public URL

**Deployment Pipeline:**
```
Local Development → Build Image → Push to Docker Hub → Deploy to OnRender → Public URL
```

---

## 🚀 Getting Started

### Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Basic command line knowledge
- Text editor (VS Code recommended)
- Docker Hub account (for Module 4)
- OnRender account (for Module 4)

### Quick Start

1. **Clone or download this repository**
   ```bash
   cd Docker-Workshop-DSML
   ```

2. **Verify Docker installation**
   ```bash
   docker --version
   docker run hello-world
   ```

3. **Start with Module 1**
   ```bash
   cd module-1-docker-basics
   # Follow exercises.md
   ```

---

## 📖 Module Structure

Each module contains:
- `exercises.md` - Step-by-step hands-on exercises
- Sample code and configuration files (where applicable)
- Expected results and validation steps
- Common errors and troubleshooting tips

### Recommended Learning Path

1. **Module 1: Docker Basics** - Foundation concepts
2. **Module 2: Building Images** - Create custom containers
3. **Module 3: Docker Compose** - Multi-container apps
4. **Module 4: Cloud Deployment** - Go live!

---

## 🛠️ Tools & Technologies Used

- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration
- **Python** - Application development
- **Streamlit** - Web UI framework
- **Transformers** - Hugging Face ML library
- **DistilGPT2** - Lightweight language model
- **PostgreSQL** - Relational database
- **pgAdmin** - Database management UI
- **Docker Hub** - Container registry
- **OnRender** - Cloud deployment platform

---

## 🎓 Learning Outcomes

By completing this workshop, you will be able to:

✅ Understand Docker architecture and container concepts  
✅ Run and manage Docker containers  
✅ Create custom Docker images with Dockerfiles  
✅ Optimize images for AI/ML workloads  
✅ Orchestrate multi-container applications  
✅ Manage data persistence with volumes  
✅ Configure container networking  
✅ Deploy containerized applications to the cloud  
✅ Share your work via public URLs  
✅ Apply Docker best practices for production  

---

## 🔧 Common Commands Reference

### Basic Docker Commands
```bash
# Container management
docker run [IMAGE]              # Run a container
docker ps                       # List running containers
docker ps -a                    # List all containers
docker stop [CONTAINER]         # Stop a container
docker start [CONTAINER]        # Start a container
docker rm [CONTAINER]           # Remove a container
docker logs [CONTAINER]         # View container logs

# Image management
docker images                   # List images
docker build -t [TAG] .         # Build image
docker pull [IMAGE]             # Pull image from registry
docker push [IMAGE]             # Push image to registry
docker rmi [IMAGE]              # Remove image

# System management
docker system df                # Show disk usage
docker system prune             # Clean up unused resources
```

### Docker Compose Commands
```bash
docker-compose up -d            # Start services in background
docker-compose down             # Stop services
docker-compose ps               # List services
docker-compose logs [SERVICE]   # View service logs
docker-compose restart [SERVICE] # Restart a service
docker-compose down -v          # Remove services and volumes
```

---

## ⚠️ Common Issues & Solutions

### Port Already in Use
```bash
# Find what's using the port
docker ps

# Use a different port
docker run -p 8080:80 nginx  # Change 8080 to another port
```

### Container Name Conflict
```bash
# Remove existing container
docker rm -f [CONTAINER_NAME]

# Or use a different name
docker run --name myapp-v2 nginx
```

### Cannot Connect to Docker Daemon
- Ensure Docker Desktop is running
- On Linux: `sudo systemctl start docker`

### Out of Disk Space
```bash
# Clean up unused containers and images
docker system prune -a --volumes
```

---

## 🎯 Projects Built in This Workshop

### 1. Story Generator TinyLLM App (Module 2)
- AI-powered story generation
- Uses DistilGPT2 model
- Streamlit web interface
- Optimized for low memory (512MB)

### 2. E-Commerce Database Stack (Module 3)
- PostgreSQL database
- pgAdmin web interface
- Sample e-commerce data
- Persistent volume storage

### 3. Cloud-Deployed LLM App (Module 4)
- Publicly accessible AI app
- HTTPS enabled
- Global deployment
- Production-ready

---

## 📝 Workshop Tips

### For Beginners
- Take your time with Module 1
- Run each command and observe the output
- Read error messages carefully
- Use `docker ps -a` frequently to check container status

### For Intermediate Users
- Focus on Dockerfile optimization in Module 2
- Understand networking in Module 3
- Experiment with different configurations

### For All Levels
- Clean up containers regularly
- Check logs when things don't work
- Use `docker inspect` to debug
- Practice the commands multiple times

---

## 🌟 Next Steps After Workshop

1. **Build Your Own ML App**
   - Containerize an existing project
   - Try different ML frameworks (TensorFlow, scikit-learn)
   - Optimize for your specific use case

2. **Explore Advanced Topics**
   - Kubernetes for orchestration
   - Docker Swarm for clustering
   - CI/CD pipelines with Docker
   - Security scanning and best practices

3. **Production Considerations**
   - Container monitoring and logging
   - Auto-scaling strategies
   - Load balancing
   - Database backups and disaster recovery

4. **Join the Community**
   - Docker Community Forums
   - Stack Overflow
   - GitHub repositories
   - Local Docker meetups

---

## 📚 Additional Resources

- [Docker Official Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## 🤝 Contributing

If you find issues or have suggestions for improvement:
1. Open an issue
2. Submit a pull request
3. Share your feedback

---

## 📄 License

This workshop is provided for educational purposes. Feel free to use and modify for your learning and teaching needs.

---

## 🙏 Acknowledgments

Built with ❤️ for the Data Science and Machine Learning community.
s
Special thanks to:
- Docker community for excellent documentation
- Hugging Face for making ML accessible
- Streamlit for easy web app development

---

**Ready to containerize your ML workflows? Start with Module 1!** 🚀