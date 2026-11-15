#!/bin/bash
# Deploy OpenMontage on KVM4 Server
# Run this script ON your KVM4 server

set -e

echo "=== OpenMontage KVM4 Deployment ==="

# 1. Install Docker + NVIDIA Container Toolkit
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER
    echo "Docker installed. You may need to log out/in or run: newgrp docker"
else
    echo "Docker already installed"
fi

# Install NVIDIA Container Toolkit
if ! dpkg -l | grep -q nvidia-container-toolkit; then
    echo "Installing NVIDIA Container Toolkit..."
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \n      sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \n      sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
else
    echo "NVIDIA Container Toolkit already installed"
fi

# 2. Create project directory
mkdir -p ~/openmontage && cd ~/openmontage

# 3. Copy Docker files (you'll need to copy them from this project)
echo "Copy Dockerfile and docker-compose.yml to ~/openmontage/"
echo "Then run: docker compose -f docker-compose.yml build"
echo "Then run: docker compose -f docker-compose.yml up -d"

# 4. Build and run (run these after copying files)
# docker compose -f docker-compose.yml build
# docker compose -f docker-compose.yml up -d

# 5. Enter container
# docker exec -it openmontage bash

# 6. Inside container - test
# source .venv/bin/activate
# python -c "from tools.tool_registry import registry; registry.discover(); print('OpenMontage ready!')"

# 7. Run demo (zero-API-key)
# make demo

echo "=== Deployment script complete ==="
echo "Copy the Dockerfile and docker-compose.yml to your KVM4 server and run the build/up commands."
