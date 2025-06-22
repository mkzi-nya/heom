#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
# 清空旧的输出文件
> "../heom.txt"
> "../heom.dict.yaml"
> "../ziys/heom.txt"
> "../ziys/heom.dict.yaml"

for file in 1.txt 2.txt; do
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
for file in ../heom.txt ./3.txt ./4.txt ./5.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../ziys/heom.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done

for file in ../heom.txt ./4.txt ./5.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../ziys/heom.dict.yaml"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done
sort --stable -t '	' -k2,2 ../heom.txt > ../heom_s.txt
sort --stable -t '	' -k2,2 ../ziys/heom.txt > ../ziys/heom_s.txt
cd "$OLD_DIR"