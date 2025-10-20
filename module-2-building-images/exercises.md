### What You'll Learn:
- Why we need custom images
- Basic Dockerfile syntax
- How to build and run custom images
- Layer caching concepts

### Instructions

**Step 1**: Create a simple Dockerfile
```bash
mkdir dockerfile-basics
cd dockerfile-basics
```

Create a file called `hello.txt`:
```bash
echo "Hello from my custom Docker image!" > hello.txt
```

Create a `Dockerfile`:
```dockerfile
FROM ubuntu:20.04
RUN apt-get update && apt-get install -y curl
COPY hello.txt /app/
WORKDIR /app
CMD ["cat", "hello.txt"]
```

**Step 2**: Build and run your first custom image
```bash
docker build -t my-first-image .
docker run my-first-image
```

**Step 3**: Understand what happened
```bash
# See your custom image
docker images | grep my-first-image

# See the build history
docker history my-first-image
```

### Expected Result
- You created your first custom Docker image
- You understand basic Dockerfile syntax
- You can see the image layers

### What You Learned:
- [ ] Dockerfile is like a recipe for building images
- [ ] `FROM` specifies the base image
- [ ] `RUN` executes commands during build
- [ ] `COPY` copies files into the image
- [ ] `WORKDIR` sets the working directory
- [ ] `CMD` specifies what runs when container starts

### Common Mistakes to Avoid:
- ❌ Not understanding that each instruction creates a layer
- ❌ Forgetting to use `WORKDIR` before copying files
- ❌ Not optimizing layer order for caching

## Exercise 1: Build the Story Generator TinyLLM App

### What You'll Learn:
- How to build complex applications with Docker
- Dockerfile optimization for AI/ML workloads
- Layer caching for large dependencies
- Production-ready Dockerfile best practices

### Instructions

**Step 1**: Navigate to sample app directory
```bash
cd modules-2hr-compressed/sample-app
```

**Step 2**: Examine the `app.py`
Take a look at the Story Generator application. Key features:
- Uses DistilGPT2 (80MB lightweight LLM)
- Streamlit chat interface
- Story generation with "Once upon a time..."
- Optimized for 512MB RAM

**Step 3**: Review `requirements.txt`
```txt
streamlit==1.29.0
transformers==4.35.0
torch==2.1.0+cpu
sentencepiece==0.1.99
accelerate==0.24.1
```

**Step 4**: Examine the `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
# Install CPU-only PyTorch first (much smaller and faster)
RUN pip install torch==2.1.0+cpu torchvision==0.16.0+cpu torchaudio==2.1.0+cpu --index-url https://download.pytorch.org/whl/cpu
# Install remaining dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY app.py .

# Create non-root user for security
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]
```

**Key Dockerfile Concepts Explained:**
- `FROM python:3.11-slim`: Base image (lightweight Python)
- `WORKDIR /app`: Set working directory
- `COPY requirements.txt .`: Copy dependencies first (layer caching!)
- `RUN pip install...`: Install Python packages
- `COPY app.py .`: Copy application code last (changes frequently)
- `USER user`: Security best practice (non-root user)
- `HEALTHCHECK`: Monitor application health
- `EXPOSE 8501`: Document the port (doesn't actually expose it)
- `CMD`: What runs when container starts

**Step 5**: Build the image
```bash
docker build -t story-generator:v1 .
```

This will take 3-5 minutes for the first build as it downloads PyTorch and the transformer models. Watch the layers being created!

**What's happening during build:**
- Downloads base Python image
- Installs system dependencies (cached layer)
- Installs PyTorch (large layer, but cached!)
- Installs other Python packages
- Copies application code (small layer, changes frequently)

**Step 6**: Run it
```bash
docker run -d --name story-generator-app -p 8501:8501 story-generator:v1
```

**Step 7**: Test it
```bash
# Check if running
docker ps | grep story-generator

```bash
# View logs to see model loading
docker logs -f story-generator-app
```

**Step 8**: Try generating a story!
- Open http://localhost:8501
- Wait for model to load (you'll see "Loading model..." then "✓ Model loaded successfully!")
- Type a story idea like: "a brave knight"
- Watch as the AI generates a story starting with "Once upon a time..."

### Expected Result
- ✅ Image builds successfully (~3-5 minutes)
- ✅ Container runs without errors
- ✅ Streamlit app loads at http://localhost:8501
- ✅ DistilGPT2 model loads successfully
- ✅ You can generate AI stories!

### What You Learned:
- [ ] How to build complex AI/ML applications with Docker
- [ ] Dockerfile optimization for large dependencies
- [ ] Layer caching strategy (dependencies first, code last)
- [ ] Security best practices (non-root user)
- [ ] Health checks for production readiness
- [ ] How to handle large model downloads

### Common Mistakes to Avoid:
- ❌ Not copying requirements.txt first (breaks layer caching)
- ❌ Installing dependencies after copying code
- ❌ Running as root user (security risk)
- ❌ Not using health checks for long-running apps
- ❌ Forgetting to expose ports properly