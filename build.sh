#!/usr/bin/env bash
# build.sh — يُنفَّذ مرة واحدة عند البناء على Render

set -e

echo "==> Installing system packages..."
apt-get update -qq
apt-get install -y --no-install-recommends ffmpeg > /dev/null 2>&1
echo "==> ffmpeg installed"

echo "==> Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r r3d.txt -q
echo "==> Python deps installed"

echo "==> Build complete"
