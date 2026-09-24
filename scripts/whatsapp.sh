#!/usr/bin/env bash
# WhatsApp-safe re-encode: H.264 Main 4.0, AAC 44.1k, faststart, target < 16 MB so it sends as a playable video.
set -e; in="$1"; out="${in%.mp4}_whatsapp.mp4"
ffmpeg -v error -y -i "$in" -c:v libx264 -profile:v main -level 4.0 -preset medium -crf 22 -pix_fmt yuv420p -c:a aac -b:a 128k -ar 44100 -movflags +faststart "$out"
ls -la "$out"
