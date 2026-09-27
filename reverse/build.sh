#!/bin/bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
echo "[*] apktool b -> dist/nya_rebuild.apk"
mkdir -p dist
apktool b . -o dist/nya_rebuild.apk
echo "[*] built $(du -h dist/nya_rebuild.apk)"
echo "[*] verify:"
apktool d dist/nya_rebuild.apk -o /tmp/verify_rebuild -f >/dev/null 2>&1 && echo "  apktool d ok"
echo "[*] to sign: apksigner sign --ks debug.keystore --ks-pass pass:android dist/nya_rebuild.apk"
echo "[*] or: jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA256 -keystore debug.keystore dist/nya_rebuild.apk android"
