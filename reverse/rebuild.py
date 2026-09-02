#!/usr/bin/env python3
import tarfile, io, os, subprocess, pathlib, zipfile
ROOT = pathlib.Path(__file__).parent
# 1. 如改了 _logic/nya_extracted，可重打nya.tar
src = ROOT / "_logic" / "nya_extracted" / "ime_data_dir"
dst = ROOT / "assets" / "nya.tar"
# 已修复：不再自动重打 nya.tar（原逻辑用 PAX 导致 ?文件名、空键盘），如需改动请手动用 GNU_FORMAT 增量替换
# if src.exists():
#     ...
# 2. apktool build
subprocess.run(["apktool","b",str(ROOT),"-o",str(ROOT/"dist"/"nya_rebuild.apk")], check=True)
print("[*] built dist/nya_rebuild.apk", (ROOT/"dist"/"nya_rebuild.apk").stat().st_size)

# 3. 自动提取heom覆盖示例：把仓库code/heom.txt同步到nya.tar
# cp ../heom.txt -> _logic/nya_extracted/...
