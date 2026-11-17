# Dockerfile.openmontage
# OpenMontage (calesthio/OpenMontage) - AGPL-3.0
# Agentic video production framework

FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.10

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \n    python3.10 python3.10-venv python3.10-dev \n    nodejs npm \n    ffmpeg \n    git curl wget \n    build-essential \n    && rm -rf /var/lib/apt/lists/*

# Set python3.10 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \n    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Install uv for fast pip
RUN pip install --no-cache-dir uv

# Create app user
RUN useradd -m -s /bin/bash openmontage
WORKDIR /home/openmontage

# Clone OpenMontage
USER openmontage
RUN git clone https://github.com/calesthio/OpenMontage.git /home/openmontage/OpenMontage
WORKDIR /home/openmontage/OpenMontage

# Create virtual environment and install dependencies
RUN uv venv --python 3.10 .venv
ENV PATH="/home/openmontage/OpenMontage/.venv/bin:$PATH"

# Install Python dependencies
RUN uv pip install -r requirements.txt

# Install GPU dependencies (optional - for NVIDIA GPU)
# RUN uv pip install -r requirements-gpu.txt
# RUN uv pip install diffusers transformers accelerate

# Install Remotion composer
RUN cd remotion-composer && npm install

# Install Piper TTS (offline)
RUN uv pip install piper-tts || echo "piper-tts optional"

# Warm HyperFrames cache
RUN npx --yes hyperframes --version >/dev/null 2>&1 || echo "HyperFrames cache warm skipped"

# Copy .env.example to .env
RUN cp .env.example .env

# Default command
CMD ["/bin/bash"]
