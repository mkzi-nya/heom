#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
sh 拼接.sh
cp "../ziys/heom.schema.yaml" "/Users/mingzi/Library/Rime"
cp "../ziys/heom.dict.yaml" "/Users/mingzi/Library/Rime"
cp "../heom.txt" "../android/鹤仓/"
sh 转格式.sh
cd "$OLD_DIR"
