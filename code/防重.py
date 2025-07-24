#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本功能：读取00.txt，根据编码长度和前缀过滤，按规则将映射结果输出到01.txt和02.txt。
"""

from collections import Counter, defaultdict

def main():
    input_file = '00.txt'
    output_file1 = '01.txt'
    output_file2 = '02.txt'

    # 1. 读取并解析所有行
    entries = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                continue
            char, code = parts
            entries.append((char, code))

    # 2. 只保留长度为4且不以"of"开头的编码
    valid = [(char, code) for char, code in entries
             if len(code) == 4 and not code.startswith('of')]

    # 3. 统计原始编码出现次数，用于后续确保每个变体最多3次
    original_counts = Counter(code for char, code in valid)
    assigned_counts = dict(original_counts)  # 初始就把原始也算进去

    # 4. 按原编码分组
    groups = defaultdict(list)
    for char, code in valid:
        groups[code].append(char)

    # 5. 生成所有可能的变体编码（按顺序尝试）
    def gen_variants(code):
        c1, c2, c3, c4 = code
        return [
            f"{c1}{c2}{c3}x",  # abdx
            f"{c1}{c2}{c3}z",  # abdz
            f"{c1}{c2}{c4}",  # abdx
            f"{c1}{c2}{c4}",  # abdz
            f"{c1}{c2}x{c3}",  # abdx
            f"{c1}{c2}z{c3}",  # abdz
            f"{c1}{c2}x{c4}",  # abdx
            f"{c1}{c2}z{c4}",  # abdz
            f"{c1}{c2}{c3}{c4}a",  # abdx
            f"{c1}{c2}{c3}{c4}b",  # abdz
            f"{c1}{c2}{c3}{c4}c",  # abdx
            f"{c1}{c2}{c3}{c4}d",  # abdz
        ]

    # 6. 打开输出文件，逐组处理
    with open(output_file1, 'w', encoding='utf-8') as f1, \
         open(output_file2, 'w', encoding='utf-8') as f2:

        for code, chars in groups.items():
            # 如果这个编码组总数<=3，跳过（不写01.txt，也不写02.txt）
            if len(chars) <= 3:
                continue

            # 前3个原封不动，不输出
            leftovers = chars[3:]

            # 按顺序给每个变体分配，确保每个变体编码最多出现3次
            for var in gen_variants(code):
                if not leftovers:
                    break
                exist = assigned_counts.get(var, 0)
                if exist >= 3:
                    continue
                allow = 3 - exist  # 还能分配多少
                to_assign = leftovers[:allow]
                for ch in to_assign:
                    f1.write(f"{ch}\t{var}\n")
                assigned_counts[var] = exist + len(to_assign)
                leftovers = leftovers[allow:]

            # 如果还有剩余，写到02.txt，保留原始编码
            for ch in leftovers:
                f2.write(f"{ch}\t{code}\n")

if __name__ == '__main__':
    main()
