#!/bin/bash

# Asteroids Game Web Build Script
echo "🚀 Building Asteroids Game for Web..."

# Check if pygbag is installed
if ! command -v python -m pygbag &> /dev/null; then
    echo "📦 Installing pygbag..."
    pip install pygame-ce pygbag
fi

# Build the web version
echo "🔧 Compiling game to WebAssembly..."
python -m pygbag main.py \
    --width 1280 \
    --height 720 \
    --name "Asteroids Game - 1000 Levels" \
    --archive \
    --cdn "https://cdn.jsdelivr.net/pyodide/" \
    --template custom

echo "✅ Build complete!"
echo "📁 Output files are in the 'dist/' directory"
echo "🌐 Upload the 'dist/' folder to Cloudflare Pages"
echo ""
echo "🔗 For Cloudflare Pages deployment:"
echo "   1. Go to Cloudflare Pages dashboard"
echo "   2. Create new project"
echo "   3. Upload the 'dist/' folder contents"
echo "   4. Set custom domain (optional)"
echo ""
echo "🎮 Your game will be available at your Cloudflare Pages URL!"
