#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
sh 拼接.sh
cp "../ziys/heom.txt" "../../IME-Converter-web/dict/ziys-heom.txt"
cp "../heom.txt" "../../IME-Converter-web/dict/heom.txt"
cp "../ziys/heom.schema.yaml" "/Users/mingzi/Library/Rime"
cp "../ziys/heom.dict.yaml" "/Users/mingzi/Library/Rime"
cp "../heom.txt" "../android/鹤仓/"
sh push.sh
cd "$OLD_DIR"
