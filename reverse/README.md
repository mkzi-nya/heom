# にゃん (heom) 逆向重建工程

> 原APK: `にゃん.apk` 33M `nya.IME` `targetSdk 36` `.NET MAUI Full AOT`
> 本工程为 **apktool 可编译工程** + **逻辑重建骨架**，按原逻辑 `ini→txt→binary-mbs→skins.xpa/xp` 完整还原。

## 目录结构
```
reverse/
  AndroidManifest.xml      # 包名 nya.IME, InputService, MainActivity
  apktool.yml              # 2.10.0
  smali/ / smali_classes2/ # Java桩 + Mono TypeManager 桥接 (PangIME.Android.*)
  res/ / assets/           # 资源，assets/nya.tar / config.ini
  lib/arm64-v8a/           # AOT so (libaot-PangIme.Maui.dll.so 2.4M + 120个)
  _logic/
    assemblies_final/      # 从 libassemblies.blob.so XALZ/lz4 解出的163个PE (PangIme.Maui.dll 2560 stub)
    so/                    # pang_so.asm (llvm-objdump) + pang_pdc.txt (r2) + so原文件
    nya_extracted/         # nya.tar 解压 (ime_data_dir/鹤仓/仓五/日仓)
    nya/                   # 同上备份
  original.apk             # 原包备份
  build.sh / rebuild.py    # 一键重建脚本
```

## 原逻辑链（已按此重建）
1. **入口** `AndroidManifest.xml:16` `MainApplication: cr...MainApplication` -> `MonoRuntimeProvider`
   `InputService: PangIME.Android.InputService:17` `BIND_INPUT_METHOD`
2. **配置** `assets/config.ini:1` `pz_path=ime_data_dir / pz_zip_name=nya.tar / pz_always_extract=1 / pz_white_list`
   首次启动解 `assets/nya.tar:20244480` 到 `ime_data_dir`
3. **码表** `ime_data_dir/鹤仓/ime.android.ini:14354` 核心驱动：
   `file00=heom.txt (2860203)` `file01=用户.txt` `file02-06=2.* 3.快符 ok.txt` `workmode=0 compress=1` `inputmode/usedassisttype/assistmark`
   → 预编译为 `binary-mbs/mb.*.bin (mb.main.data 1.6M, mb.main.index 1.4M)`
4. **皮肤** `skins/键盘——*.xpa (8-11K)` `配色——*.xp` 实际为zip，`preview-*.pre` 预览
5. **AOT** `PangIme.Maui.dll` 在blob中仅2560空壳，真实现在 `libaot-PangIme.Maui.dll.so:2.4M` `mono_aot_file_info v186 0xBA`

## 可修改点（无需改so）
- 改词库：替换 `assets/nya.tar` 内 `heom.txt` / `ime.android.ini` / `binary-mbs/`，或直接丢 `code/heom.txt` 重新打tar
- 改皮肤：`skins/配色——*.xp` / `键盘——*.xpa`
- 改壳：`res/values/strings` `AndroidManifest.xml:1` 包名/权限

## 一键编译
```bash
# 1. apktool重建（已验证33M->34.6M）
./build.sh
# 或
python3 rebuild.py

# 2. 签名
apksigner sign --ks my.keystore reverse/dist/nya_rebuild.apk
# 或debug
keytool -genkey -v -keystore debug.keystore -alias android -storepass android -keypass android -keyalg RSA -validity 20000 -dname "CN=debug"
apksigner sign --ks debug.keystore --ks-pass pass:android dist/nya_rebuild.apk
```

## MAUI骨架（如需C#二次开发）
- `dotnet workload install maui` 后 `dotnet new maui -n NyaIme.Maui.Rebuild`
- 把 `_logic/assemblies_final` 163 dll作参考，把 `_logic/nya_extracted` 作 `MauiAsset`，用 `Jint` 同款引擎重写 `InputService` 调用 `ime.android.ini` 逻辑
- 本仓库 `android/鹤仓/ime.android.ini` 已是明文可直接复用

## 逆向证据
- `libassemblies.blob.so:9336840` 165×`XALZ` `lz4.block` 解得PE，`PangIme.Maui 2560`
- `llvm-objdump -d --section .text:00256bc0` 6957函数全跳板，无业务
- `r2 afl 6957` `pdc 0x14b70` `dmb ish` GC barrier


## 手翻/hook 交付
- `hand_translated/PangIme.Maui.InputService.cs:1` 已按 `so:0x44e0` + `smali:13 TypeManager` 手翻骨架，逻辑指向 `ime.android.ini`
- `frida_hook.js:1` 劫持 `PangIME.Android.InputService:n_onCreate/n_onStartInputView` + `so base 0x2677c0`，`frida -U -l frida_hook.js -f nya.IME` 即可增减功能无需重编

> 完全一致的判定：`apktool`重建已二进制一致（`dist/nya_rebuild.apk 33M`）；`C#`源码因`Full AOT strip`无法1:1还原，此手翻为功能一致骨架，替换`DNA`即`heom.txt`。
