#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
awk -F'\t' '{print $2 "\t" $1}' ../heom_s.txt > ../heom_s_1.txt
awk -F'\t' '{print $2 "\t" $1}' ../ziys/heom_s.txt > ../ziys/heom_s_1.txt
cd "$OLD_DIR"
