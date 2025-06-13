#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
# 清空旧的输出文件
> "../heom.txt"
> "../heom.dict.yaml"

# 按顺序拼接 1.txt 2.txt 3.txt
for file in 1.txt 2.txt 3.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../heom.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done

for file in 0.txt ../heom.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../heom.dict.yaml"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done
sort -s -t $'\t' -k2,2 ../heom.txt > ../heom_s.txt
cd "$OLD_DIR"