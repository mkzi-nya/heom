#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
# 清空旧的输出文件
> "../heom.txt"
> "../heom.dict.yaml"
> "../ziys/heom.txt"
> "../ziys/heom.dict.yaml"
> "../android/鹤仓/用户.txt"
> "../android/鹤仓/ok.txt"
> "../heom_无ok拼字.txt"

for file in 1.txt 2.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../heom.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done

python 防重.py

for file in ../heom.txt 3.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../heom_无ok拼字.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done
for file in 3.txt 4.txt; do
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

for file in ../heom.txt ./5.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../ziys/heom.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done

for file in ./5.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../android/鹤仓/用户.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done

for file in ../heom.dict.yaml ./5.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "../ziys/heom.dict.yaml"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done
cp ../heom_无ok拼字.txt ../android/鹤仓/heom.txt
cp ./4.txt ../android/鹤仓/ok.txt
sort --stable -t '	' -k2,2 ../heom.txt > ../heom_s.txt
sort --stable -t '	' -k2,2 ../ziys/heom.txt > ../ziys/heom_s.txt
awk -F'\t' '{gsub(/\r/,""); print $2 "\t" $1}' ../heom_s.txt > ../heom_s_1.txt
awk -F'\t' '{gsub(/\r/,""); print $2 "\t" $1}' ../ziys/heom_s.txt > ../ziys/heom_s_1.txt

cd "$OLD_DIR"