#!/bin/bash

# Build script for Cloudflare Pages
echo "Building Asteroids game for web..."

# Install Python dependencies
pip install pygame-ce pygbag

# Change to web directory
cd web

# Build with pygbag
python -m pygbag main.py \
  --width 1280 \
  --height 720 \
  --name "Asteroids Game - 1000 Levels" \
  --archive \
  --ume_block 0

echo "Build complete!"
