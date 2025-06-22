count = 0
with open('2.txt', encoding='utf-8') as f:
    keys_to_remove = {line.strip().split('\t')[0] for line in f}

with open('1.txt', encoding='utf-8') as fin, open('1_cleaned.txt', 'w', encoding='utf-8') as fout:
    for line in fin:
        key = line.strip().split('\t')[0]
        if key in keys_to_remove:
            print(f"Removed line with key: {key}")
            count += 1
        else:
            fout.write(line)

print(f"Total removed lines: {count}")
