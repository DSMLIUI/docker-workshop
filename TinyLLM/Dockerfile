# T5-efficient-tiny ChatGPT Interface
# Optimized for 512MB RAM (Render Free Tier)

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

# Note: GPT-2 Small model will be downloaded at runtime
# This avoids build timeouts and makes builds more reliable

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
     "--server.headless=true", \
     "--server.enableXsrfProtection=false", \
     "--browser.gatherUsageStats=false", \
     "--server.runOnSave=false"]