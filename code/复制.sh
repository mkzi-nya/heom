#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
cp "../heom.txt" "../../IME-Converter-web/dict/ziys-heom.txt"
cp "../heom.txt" "../安卓/FlyPY_pro/小鹤音形/ziys-heom.txt"
cp "../heom.txt" "/storage/emulated/0/FlyPY_pro/小鹤音形/ziys-heom.txt"
cd "$OLD_DIR"
