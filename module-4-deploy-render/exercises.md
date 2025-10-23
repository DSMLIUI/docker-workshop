## Exercise 0.5: Understanding Cloud Deployment

### Task
Learn why we need cloud deployment and what the deployment pipeline looks like.

### What You'll Learn:
- Why we need cloud deployment
- What Docker Hub is and why we use it
- How registries work
- What OnRender provides
- The deployment pipeline

### Instructions

**Step 1**: Understand the problem
- Your app works locally
- But how do others access it?
- How do you share your containerized app?

**Step 2**: The solution
- **Docker Hub**: Share your images publicly
- **OnRender**: Run your containers in the cloud
- **Public URL**: Anyone can access your app

**Step 3**: The deployment pipeline
```
Local Development → Docker Image → Docker Hub → Cloud Platform → Public URL
```

### Expected Result
- You understand why we need cloud deployment
- You see the deployment pipeline
- You're ready to deploy your app

## 📌 Deployment Overview

In this module, you'll:
1. **Tag** your Docker image properly
2. **Push** to Docker Hub (public registry)
3. **Deploy** to OnRender from Docker Hub
4. **Get** a live public URL to share!

This is the standard workflow for deploying containerized applications to the cloud.

## Exercise 1: Prepare Your Docker Image

### Task
Ensure your LLM Story Generator image is built and ready.

### What You'll Learn:
- How to verify Docker images before deployment
- Local testing before cloud deployment
- Image tagging best practices
- Pre-deployment validation

### Instructions

**Step 1**: Navigate to the sample app
```bash
cd modules-2hr-compressed/sample-app
```

**Step 2**: Verify your Dockerfile exists
```bash
ls -la Dockerfile
```

**Step 3**: Build the image (if not already built)
```bash
docker build -t story-generator:latest .
```

This may take 3-5 minutes if not cached.

**Step 4**: Test it locally
```bash
docker run -d --name story-test -p 8501:8501 myllm:latest

# Wait 30-60 seconds for model to load, then test
curl http://localhost:8501

# Clean up
docker stop story-test && docker rm story-test
```

### Expected Result
- ✅ Image builds successfully
- ✅ Container runs locally
- ✅ Story Generator works at http://localhost:8501
- ✅ Ready to push to Docker Hub

## Exercise 2: Create Docker Hub Account

### Task
Set up a Docker Hub account to host your image publicly.

### Instructions

**Step 1**: Visit [hub.docker.com](https://hub.docker.com)

**Step 2**: Click "Sign Up"

**Step 3**: Create your account
- Choose a username (you'll use this in image names!)
- Email and password
- Verify email

**Step 4**: Note your Docker Hub username
Example: If your username is `johndoe`, your images will be `johndoe/image-name`

### Expected Result
- ✅ Docker Hub account created
- ✅ Username noted
- ✅ Ready to push images

## Exercise 3: Push Image to Docker Hub (5 minutes)

### Task
Tag and push your LLM image to Docker Hub so OnRender can pull it.

### Instructions

**Step 1**: Login to Docker Hub from terminal
```bash
docker login
# Enter your Docker Hub username
# Enter your Docker Hub password
```

You should see "Login Succeeded"!

**Step 2**: Tag your image with your Docker Hub username
```bash
# Replace YOUR_USERNAME with your actual Docker Hub username
docker tag myllm:latest YOUR_USERNAME/myllm:latest

# Example: docker tag myllm:latest johndoe/myllm:latest
```

**Step 3**: Push to Docker Hub
```bash
docker push YOUR_USERNAME/myllm:latest
```

**Step 4**: Verify on Docker Hub
- Visit https://hub.docker.com/r/YOUR_USERNAME/myllm
- You should see your image listed!

### Expected Result
- ✅ Logged into Docker Hub
- ✅ Image tagged correctly
- ✅ Image pushed successfully  
- ✅ Visible on Docker Hub website
- ✅ Public URL: `YOUR_USERNAME/myllm:latest`

### Create GROQ_API_KEY from [grow](https://groq.com) - Save it somewhere

### Create OnRender Account 

# Congrats for completing the workshop