#!/bin/bash
# start.sh — تشغيل البوت على Replit

# تثبيت FFmpeg إذا لم يكن موجوداً
if ! command -v ffmpeg &> /dev/null; then
    echo "Installing ffmpeg..."
    apt-get install -y ffmpeg 2>/dev/null || nix-env -iA nixpkgs.ffmpeg
fi

# تثبيت المكتبات
pip install -q -r r3d.txt

# تشغيل البوت
python3 main.py
