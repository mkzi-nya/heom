#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
cp "../ziys/heom.txt" "../../IME-Converter-web/dict/ziys-heom.txt"
cp "../heom.txt" "../../IME-Converter-web/dict/heom.txt"
cp "../heom.txt" "/storage/emulated/0/FlyPY_pro/鹤仓/heom.txt"
cp "../ziys/用户.txt" "/storage/emulated/0/FlyPY_pro/鹤仓/用户.txt"
cd "$OLD_DIR"
