# 手翻说明
- 源码：libaot-PangIme.Maui.dll.so .text:00256bc0 6957跳板，无名，已用 llvm-objdump + r2 pdc 翻为 PangIme.Maui.InputService.cs 骨架
- 真逻辑不在C#在 ime.android.ini + heom.txt + binary-mbs，已在 _logic/nya_extracted 完整保留，直接复用即可达到与原app一致
- 要完全一致：用本reverse的 apktool 工程即二进制一致；C#层此手翻骨架补齐接口即可编译，`dotnet new maui` 后替换即可
