#!/bin/bash
OLD_DIR="$(pwd)"
cd "$(cd "$(dirname "$0")" && pwd)"
cp "../ziys/heom.schema.yaml" "/Users/mingzi/Library/Rime"
cp "../ziys/heom.dict.yaml" "/Users/mingzi/Library/Rime"
cd "$OLD_DIR"
