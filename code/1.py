def process_file(input_file='./2.txt', reference_file='./1.txt', output_file='./2-1.txt'):
    # 读取1.txt内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    for line in lines:
        if '\t' in line:
            char, code = line.strip().split('\t')
            entries.append((char, code))

    # 读取2.txt并构建 char -> set(codes) 映射
    ref_map = {}
    with open(reference_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                char, code = line.strip().split('\t')
                if char not in ref_map:
                    ref_map[char] = set()
                ref_map[char].add(code)

    to_remove = set()

    for char, code in entries:
        if len(code) >= 2 and char in ref_map:
            for ref_code in ref_map[char]:
                if code.startswith(ref_code) and code != ref_code:
                    to_remove.add((char, code))
                    break

    # 写入被剪切的行
    with open(output_file, 'w', encoding='utf-8') as f:
        for char, code in to_remove:
            f.write(f'{char}\t{code}\n')

    # 重写1.txt，删除被剪切的行
    with open(input_file, 'w', encoding='utf-8') as f:
        for char, code in entries:
            if (char, code) not in to_remove:
                f.write(f'{char}\t{code}\n')

if __name__ == "__main__":
    process_file()
