#!/bin/bash

# Script para instalar Buildozer y dependencias en Linux (Ubuntu/Mint/Debian)
# Guarda este archivo como kivy-buildozer-installer.sh
# Luego ejecútalo con: bash kivy-buildozer-installer.sh

set -e

echo "📦 Actualizando paquetes..."
sudo apt update
sudo apt upgrade -y

echo "📦 Instalando dependencias esenciales..."
sudo apt install -y \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    zip \
    unzip \
    openjdk-17-jdk \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    curl \
    libsqlite3-dev \
    pkg-config \
    libbz2-dev \
    liblzma-dev \
    libffi-dev \
    ccache

echo "🐍 Instalando Cython y Virtualenv..."
pip3 install --upgrade pip setuptools wheel Cython virtualenv

echo "📱 Instalando Buildozer..."
pip3 install buildozer

echo "✅ Instalación completada"
echo "Ahora puedes iniciar un proyecto con:"
echo "   buildozer init"
echo "y compilar con:"
echo "   buildozer -v android debug"
