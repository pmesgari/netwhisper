#!/bin/bash

set -e

install_utils() {
    sudo apt update
    sudo apt install -y iputils-ping curl wget tcpdump
}

install_docker() {
    echo "🔧 Installing Docker..."

    # Install dependencies
    sudo apt-get update
    sudo apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Add Docker’s GPG key
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    # Set up the repository
    echo \
    "deb [arch=$(dpkg --print-architecture) \
    signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Add current user to docker group (no sudo needed)
    sudo usermod -aG docker $USER

    # Start Docker
    sudo systemctl enable docker
    sudo systemctl start docker

    echo "✅ Docker installation complete. You may need to log out and back in for group changes to apply."

}

install_containerlab() {
    curl -sL https://containerlab.dev/setup | sudo -E bash -s "all"
}

install_uv() {
    curl -LsSf https://astral.sh/uv/install.sh | sh
}

install_utils
install_docker
install_containerlab
install_uv