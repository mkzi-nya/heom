for file in 1.txt 2.txt 3.txt; do
    if [ -f "$file" ]; then
        cat "$file" >> "0.txt"
    else
        echo "警告：文件 $file 不存在，跳过。"
    fi
done