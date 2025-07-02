#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
sh 拼接.sh
cp "../ziys/heom.txt" "../../IME-Converter-web/dict/ziys-heom.txt"
cp "../heom.txt" "../../IME-Converter-web/dict/heom.txt"
cp "../heom.txt" "/storage/emulated/0/Android/data/nya.IME/files/ime_data_dir/鹤仓/heom.txt"
cp "../ziys/用户.txt" "/storage/emulated/0/Android/data/nya.IME/files/ime_data_dir/鹤仓/用户.txt"
cp "../heom.txt" "../android/鹤仓/"
cd "$OLD_DIR"
