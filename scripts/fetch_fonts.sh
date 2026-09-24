#!/usr/bin/env bash
# Inter 4.0 (OFL 1.1) → assets/fonts/. Run once before rendering.
set -e; d="$(dirname "$0")/../assets/fonts"; mkdir -p "$d"; t=$(mktemp -d)
curl -sL -o "$t/inter.zip" https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip
unzip -o -q "$t/inter.zip" -d "$t/inter" "extras/ttf/*"
for w in Regular Medium SemiBold Bold ExtraBold; do cp "$t/inter/extras/ttf/Inter-$w.ttf" "$d/"; done
ls "$d"
