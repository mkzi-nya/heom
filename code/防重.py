#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本功能：读取../heom.txt，根据编码长度和前缀过滤，并且跳过
那些已在1~3位编码中出现过的字符。按规则将变体编码输出到3.txt，
将超额或被过滤的条目输出到3_log.txt，并在3_log.txt末尾附加每个
成功解析的原始4位编码的数量统计。
"""

from collections import Counter, defaultdict

def gen_variants(code):
    """
    生成变体编码：
    1. {第二位}{第三位}{第四位}{a-z}
    2. {第三位}{第四位}{a-z}{a-z}
    """
    c1, c2, c3, c4 = code
    variants = []

    # 第一组：{2}{3}{4}{a-z}
    for i in range(ord('a'), ord('z') + 1):
        variants.append(f"{c1}{c2}{c3}{chr(i)}")

    # 第二组：{3}{4}{a-z}{a-z} (26 * 26)
    for i in range(ord('a'), ord('z') + 1):
        for j in range(ord('a'), ord('z') + 1):
            variants.append(f"{c1}{c2}{c4}{chr(i)}")
    for i in range(ord('a'), ord('z') + 1):
        for j in range(ord('a'), ord('z') + 1):
            variants.append(f"{c1}{c2}{chr(i)}{chr(j)}")
    return variants


def main():
    input_file  = '../heom.txt'
    output_1    = '3.txt'
    output_2    = '3_log.txt'

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

    # 2. 建立 char -> set(codes) 映射
    char_to_codes = defaultdict(set)
    for char, code in entries:
        char_to_codes[char].add(code)

    # 3. 按新规则找出需要跳过的字符
    skip_chars = set()
    for char, codes in char_to_codes.items():
        # 找出该字符的所有短码（长度1-3）
        short_codes = [c for c in codes if len(c) < 4]
        # 找出该字符的所有4位码
        four_codes = [c for c in codes if len(c) == 4]
        # 判断是否存在短码作为4位码的前缀
        for sc in short_codes:
            for fc in four_codes:
                if fc.startswith(sc):
                    skip_chars.add(char)
                    break
            if char in skip_chars:
                break

    # 4. 过滤出“有效”4位编码（长度=4、非"of..."或"oi..."，且字符不在 skip_chars 中）
    valid = [
        (char, code)
        for char, code in entries
        if len(code) == 4
           and not code.startswith('of')
           and not code.startswith('oi')
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
            if len(chars) <= 3:
                continue

            # 前3个原封不动，不写入任何文件；剩下的作为 leftovers 分配变体
            leftovers = chars[3:]
            for var in gen_variants(code):
                if not leftovers:
                    break
                if assigned_counts.get(var, 0) >= 1:  # 已有则跳过
                    continue
                ch = leftovers.pop(0)                 # 取一个字符
                f1.write(f"{ch}\t{var}\n")
                assigned_counts[var] = 1              # 标记该变体已分配

            # 如果还有剩余，写到 3_log.txt（保留原始编码）
            for ch in leftovers:
                f2.write(f"{ch}\t{code}\n")

        # 8. 在3_log.txt末尾，写入“成功解析”的原始编码统计（按数量从大到小排序）
        f2.write("\n# 原始编码数量统计（仅列出分组大小 > 3 的编码）\n")
        for code, cnt in sorted(parsed_codes.items(), key=lambda x: x[1], reverse=True):
            f2.write(f"{code}\t{cnt}\n")

if __name__ == '__main__':
    main()
