#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本功能：读取../heom_s.txt，根据编码长度和前缀过滤，并且跳过
那些已在1~3位编码中出现过的字符。按规则将变体编码输出到01.txt，
将超额或被过滤的条目输出到02.txt，并在02.txt末尾附加每个
成功解析的原始4位编码的数量统计。
"""

from collections import Counter, defaultdict

def gen_variants(code):
    """生成变体编码的优先顺序"""
    c1, c2, c3, c4 = code
    return [
        f"{c1}{c2}{c4}x",
        f"{c1}{c2}{c4}z",
        f"{c1}{c2}{c3}x",
        f"{c1}{c2}{c3}z",
        f"{c1}{c2}x{c4}",
        f"{c1}{c2}z{c4}",
        f"{c1}{c2}x{c3}",
        f"{c1}{c2}z{c3}",
        f"{c1}{c2}zx",
        f"{c1}{c2}zz",
        f"{c1}{c2}{c3}{c4}a",
        f"{c1}{c2}{c3}{c4}b",
        f"{c1}{c2}{c3}{c4}c",
        f"{c1}{c2}{c3}{c4}d"
    ]

def main():
    input_file  = '../heom_s.txt'
    output_1    = '01.txt'
    output_2    = '02.txt'

    # 1. 读取原始条目
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

    # 2. 建立 char -> set(codes) 映射，用于检测短码
    char_to_codes = defaultdict(set)
    for char, code in entries:
        char_to_codes[char].add(code)

    # 3. 找出那些在1~3位编码中出现过的字符，要跳过它们所有的4位码
    skip_chars = {
        char
        for char, codes in char_to_codes.items()
        if any(len(c) < 4 for c in codes)
    }

    # 4. 过滤出“有效”4位编码（长度=4、非"of..."，且字符不在 skip_chars 中）
    valid = [
        (char, code)
        for char, code in entries
        if len(code) == 4
           and not code.startswith('of')
           and char not in skip_chars
    ]

    # 5. 按原始4位编码分组
    groups = defaultdict(list)
    for char, code in valid:
        groups[code].append(char)

    # 6. 准备计数器：原始分组大小 & 已分配次数
    original_counts = {code: len(chars) for code, chars in groups.items()}
    # 只对组大小>3的编码才算“成功解析”
    parsed_codes = {code: cnt for code, cnt in original_counts.items() if cnt > 3}
    assigned_counts = Counter(code for _, code in valid)

    # 7. 打开输出文件，逐组处理
    with open(output_1, 'w', encoding='utf-8') as f1, \
         open(output_2, 'w', encoding='utf-8') as f2:

        for code, chars in groups.items():
            # 组小于等于3：跳过（既不写01，也不写02）
            if len(chars) <= 3:
                continue

            # 前3个原封不动，不写入任何文件；剩下的作为 leftovers 分配变体
            leftovers = chars[3:]

            # 按优先级分配到 01.txt
            for var in gen_variants(code):
                if not leftovers:
                    break
                exist = assigned_counts.get(var, 0)
                if exist >= 3:
                    continue
                # 本次还能分配的数量
                allow = 3 - exist
                batch = leftovers[:allow]
                for ch in batch:
                    f1.write(f"{ch}\t{var}\n")
                assigned_counts[var] += len(batch)
                leftovers = leftovers[allow:]

            # 如果还有剩余，写到 02.txt（保留原始编码）
            for ch in leftovers:
                f2.write(f"{ch}\t{code}\n")

        # 8. 在02.txt末尾，写入“成功解析”的原始编码统计（按数量从大到小排序）
        f2.write("\n# 原始编码数量统计（仅列出分组大小 > 3 的编码）\n")
        for code, cnt in sorted(parsed_codes.items(), key=lambda x: x[1], reverse=True):
            f2.write(f"{code}\t{cnt}\n")


if __name__ == '__main__':
    main()
