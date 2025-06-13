#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
cp "../heom.schema.yaml" "/Users/mingzi/Library/Rime"
cp "../heom.dict.yaml" "/Users/mingzi/Library/Rime"
cd "$OLD_DIR"
