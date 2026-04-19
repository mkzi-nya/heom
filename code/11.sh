#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
sh 拼接.sh
cp "../android/鹤仓/heom.txt" "/storage/emulated/0/Android/data/nya.IME/files/ime_data_dir/鹤仓/heom.txt"
cp "../android/鹤仓/用户.txt" "/storage/emulated/0/Android/data/nya.IME/files/ime_data_dir/鹤仓/用户.txt"
cp "../android/鹤仓/ok.txt" "/storage/emulated/0/Android/data/nya.IME/files/ime_data_dir/鹤仓/ok.txt"
cp "../heom.txt" "../android/鹤仓/"
find ../*/ -type f -name "*.bak" -delete
sh push.sh
cd "$OLD_DIR"
