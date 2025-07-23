#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 00.txt 中形如 “字\tabcd” 的行重新分配：
* 同一编码 abcd ≥ 4 字时，保留前 3 字在 abcd，
  其余依次挪到 abdx → abdz → abxx → abxz → abzx → abzz，
  每个派生编码最多 3 字，若原本已存在则补足到 3 字为止。
结果写入 01.txt（同样一行一个“字\t编码”）。
"""
from collections import OrderedDict
from pathlib import Path

# -------- 可按需修改的参数 --------
INPUT_FILE = Path("00.txt")
OUTPUT_FILE = Path("01.txt")
MAX_PER_CODE = 3          # 每个编码最多保留 / 填充的字符数
DERIVATION_ORDER = (
    lambda a, b, c, d: [f"{a}{b}{d}x", f"{a}{b}{d}z",
                        f"{a}{b}xx",  f"{a}{b}xz",
                        f"{a}{b}zx",  f"{a}{b}zz"]
)
# ---------------------------------

def load_entries(path: Path):
    """读取文件并按出现顺序返回 [(char, code), …]。"""
    entries = []
    with path.open(encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                ch, code = line.split()
            except ValueError:
                raise ValueError(f"第 {ln} 行格式错误：{line!r}")
            entries.append((ch, code))
    return entries

def build_code_dict(entries):
    """OrderedDict: code -> [chars…]，保持首次出现的顺序。"""
    d = OrderedDict()
    for ch, code in entries:
        d.setdefault(code, []).append(ch)
    return d

def redistribute(code_dict):
    """就地调整 code_dict，使之满足分流规则。"""
    code_order = list(code_dict.keys())  # 记录输出顺序
    for code in list(code_dict.keys()):
        chars = code_dict[code]
        # 只处理四位编码，其它直接跳过
        if len(code) != 4 or len(chars) <= MAX_PER_CODE:
            continue
        a, b, c, d = code

        # 生成派生编码列表
        variants = DERIVATION_ORDER(a, b, c, d)
        src_idx = MAX_PER_CODE  # 下一枚待搬运的下标
        for vcode in variants:
            # 已有则取其列表，否则创建空列表
            vlist = code_dict.get(vcode, [])
            cap = MAX_PER_CODE - len(vlist)  # 还能装多少
            if cap > 0 and src_idx < len(chars):
                take = min(cap, len(chars) - src_idx)
                vlist.extend(chars[src_idx:src_idx + take])
                code_dict[vcode] = vlist
                if vcode not in code_order:
                    code_order.append(vcode)
                src_idx += take
                if src_idx >= len(chars):  # 源已搬空
                    break
        # 源编码只保留前 3 个
        code_dict[code] = chars[:MAX_PER_CODE]
    return code_order

def dump_entries(code_dict, order, path: Path):
    with path.open("w", encoding="utf-8") as f:
        for code in order:
            for ch in code_dict[code]:
                f.write(f"{ch}\t{code}\n")

def main():
    entries = load_entries(INPUT_FILE)
    code_dict = build_code_dict(entries)
    out_order = redistribute(code_dict)
    dump_entries(code_dict, out_order, OUTPUT_FILE)
    print(f"生成完成，共写入 {sum(len(v) for v in code_dict.values())} 行 → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
