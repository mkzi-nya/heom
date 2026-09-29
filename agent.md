# 鹤仓输入法编码实现说明

本文档面向需要阅读、修改或重新生成本仓库输入法编码的 agent/开发者。仓库名称为 `heom`，方案名为“鹤仓”：以小鹤音形的编码习惯为基础，将形码部分改为仓颉相关编码，形成 `heom` 编码。

## 1. 先看哪些文件

| 路径 | 作用 | 是否应直接编辑 |
| --- | --- | --- |
| `code/0.txt` | Rime 词库头部和 encoder 配置 | 是，配置变更时编辑 |
| `code/1.txt` | 主码表，包含标点、短码、常用字词等 | 是 |
| `code/2.txt` | 按规则扩展的单字及其编码 | 是，数据源变更时编辑 |
| `code/3.txt` | `防重.py` 生成的四码重码变体 | 通常否，由脚本生成 |
| `code/4.txt` | `ok` 前缀的仓颉拼字/查询码表 | 是，数据源变更时编辑 |
| `code/5.txt` | 用户自定义词条、短语和命令 | 是 |
| `code/拼接.sh` | 生成 Rime、Android 和排序产物 | 是，生成规则变更时编辑 |
| `code/防重.py` | 为超过三重码的四码组分配变体编码 | 是，重码算法变更时编辑 |
| `heom.schema.yaml` | Rime 方案行为配置 | 是，Rime 行为变更时编辑 |
| `heom.txt` | Rime/转换器使用的合并码表 | 否，生成产物 |
| `heom.dict.yaml` | Rime 字典，带 encoder 规则和词库头 | 否，通常由拼接脚本生成 |
| `android/鹤仓/ime.android.ini` | Android 输入法运行时配置 | 是，Android 行为变更时编辑 |
| `android/鹤仓/heom.txt` | Android 主码表 | 否，通常由拼接脚本复制生成 |
| `android/鹤仓/用户.txt` | Android 用户词库，来自 `code/5.txt` | 否，通常由拼接脚本生成 |
| `android/鹤仓/ok.txt` | Android 的 `ok` 仓颉查询码表，来自 `code/4.txt` | 否，通常由拼接脚本生成 |
| `android/鹤仓/binary-mbs/` | Android 使用的预编译码表/索引 | 不要手工改二进制内容 |
| `reverse/` | APK 逆向、解包和重建工程 | 仅在 APK/运行时相关任务中修改 |

## 2. 编码数据格式

普通码表是 UTF-8 文本，每行使用两个字段：

```text
字符或词条<TAB>编码
```

例如：

```text
鹤<TAB>heom
日<TAB>oka
```

编码通常只使用小写英文字母；`code/1.txt` 中的分号前缀条目用于符号或特殊短码。Android 和 Rime 都依赖 tab 分隔，修改时不要把 tab 替换成空格，也不要随意删除同一字符的重复编码。

### 编码来源

- `code/1.txt` 是主码表，决定常用编码和原始顺序。
- `code/2.txt` 提供扩展单字，包含大量 Unicode 汉字及多编码条目。
- `code/3.txt` 用于缓解四码重码，但它不是独立的设计来源。
- `code/4.txt` 的编码以 `ok` 开头，由 Rime 的 `cangjie` segmentor 和 Android 的独立码表使用。
- `code/5.txt` 是个人词库，既包含词条，也可能包含可执行命令、特殊字符或测试数据；修改它前应确认这些内容确实希望进入发布产物。

## 3. 生成链路

核心脚本是 `code/拼接.sh`，应从 `code/` 目录执行：

```bash
cd code
bash 拼接.sh
```

脚本执行顺序如下：

1. 清空 `heom.txt`、`heom.dict.yaml`、`ziys/` 下的对应产物，以及 Android 用户词库和 `ok.txt`。
2. 将 `code/1.txt` 和 `code/2.txt` 拼接到根目录 `heom.txt`。
3. 执行 `python 防重.py`，读取根目录 `heom.txt`，生成 `code/3.txt` 和 `code/3_log.txt`。
4. 生成 `heom_无ok拼字.txt`，即主码表加 `3.txt`，但不包含 `4.txt` 的 `ok` 拼字码。
5. 生成 `heom.dict.yaml`：先写入 `code/0.txt`，再写入当前合并码表，最后追加 `3.txt` 和 `4.txt`。
6. 生成完整 Android 主码表：`android/鹤仓/heom.txt` 来自 `heom_无ok拼字.txt`，`android/鹤仓/ok.txt` 来自 `code/4.txt`。
7. 将 `heom.txt` 和 `code/5.txt` 合并到 `ziys/` 变体，并把 `code/5.txt` 单独写入 Android 的 `用户.txt`。
8. 以编码字段排序生成 `heom_s.txt`、`ziys/heom_s.txt`，再交换字段生成对应的 `_s_1` 文件。

注意：脚本使用相对路径，并且会覆盖多个文件。不要从仓库根目录直接运行，除非先确认脚本中的路径已被调整。

## 4. 四码重码处理

`code/防重.py` 的输入是根目录 `heom.txt`，输出是 `code/3.txt` 和 `code/3_log.txt`。

处理规则：

1. 读取每行的字符和编码，按字符建立“字符到编码集合”的映射。
2. 如果一个字符同时存在短码和以短码为前缀的四码，则该字符加入跳过集合。
3. 只处理长度为四、不是 `of` 或 `oi` 前缀、且不在跳过集合中的编码。
4. 对同一个四码下的字符保留前三个，剩余字符尝试分配到变体编码。
5. 变体优先尝试类似“保留前几位并改写末位”的编码，再尝试更短前缀加两个字母的形式；已经占用的变体不会重复分配。
6. 无法分配的条目写入 `3_log.txt`，文件末尾还会记录原四码的重码数量统计。

脚本中的 `gen_variants` 是实际编码规则的唯一实现。若要改变重码策略，应同时检查生成结果、已有码表冲突以及顶屏行为；不能只修改 `3.txt` 后把它当成长期源文件。

## 5. Rime 运行方式

Rime 入口是 `heom.schema.yaml`：

- `schema_id` 为 `heom`，显示名称为“鹤仓”。
- 主 translator 使用 `heom` 字典。
- `max_code_length` 为 4，字母表为 `a-z`、分号和单引号。
- 分号是特殊短码的引导键；单引号是配置中的尾部锚点相关字符。
- `auto_select` 和 `auto_select_pattern` 控制四码顶字上屏，`ok` 前缀被排除在默认自动顶屏规则之外。
- `ok[a-z]*` 由 `cangjie` segmentor 识别，使用依赖的 `cangjie5` 字典。
- `reverse_lookup` 使用 `heom` 字典查询字符对应编码。
- `code/0.txt` 中的 encoder 规则负责由字词编码生成词组编码；`x*` 和 `z*` 编码被排除在自动编码规则之外。

将 `heom.schema.yaml` 部署到 Rime 后，还需要确保 `heom.dict.yaml`、`heom.txt` 和相关依赖字典在同一配置目录中。`default(win).yaml` 只是把 `heom` 加入方案列表，不是码表本身。

## 6. Android 运行方式

Android 版本的明文配置位于 `android/鹤仓/`。关键配置在 `ime.android.ini`：

- `imemode=0` 表示形码模式。
- `workmode=0` 表示以内存码表检索为主。
- `compress=1` 表示启用压缩码表。
- `inputmode=1` 表示使用主码表。
- `usedassisttype*` 决定辅助码表分类的检索范围。
- `push=1`、`ding=1`、`pushcodelength=4` 控制自动上屏和顶屏。
- `sysuserpath=用户.txt` 指向用户词库。
- `ok.txt`、`2.直通码表.txt`、`3.快符.txt` 等文件由运行时配置中的 `file00`、`file01` 等条目引用，完整引用关系应以 `ime.android.ini` 中对应位置为准。

Android APK 中的实际运行链路是：`assets/config.ini` 指定 `ime_data_dir` 和 `nya.tar`，应用启动时解包配置；输入服务读取 `鹤仓/ime.android.ini`，再读取文本码表或 `binary-mbs/` 中的索引和数据。`binary-mbs/` 是运行时产物，若只修改文本码表而不重新生成匹配的二进制码表，可能导致 APK 内行为与仓库明文文件不一致。

`android/更新.sh` 只会从 GitHub 下载根目录 `heom.txt` 覆盖 `android/鹤仓/heom.txt`，它不会重建 `binary-mbs/`，也不会同步 `用户.txt`、`ok.txt` 或其他辅助码表。

## 7. APK 和逆向工程

`reverse/` 保存原 APK 的 apktool 工程和逻辑分析材料。这里的实现边界很重要：

- 真正的输入逻辑主要由 `ime.android.ini`、`heom.txt`、`binary-mbs/` 和皮肤文件驱动。
- `reverse/hand_translated/PangIme.Maui.InputService.cs` 是根据 AOT 二进制和 smali 手工还原的功能骨架，不是原始 C# 源码。
- `reverse/rebuild.py` 默认只调用 apktool 重建 APK，不会自动从根目录码表重建 `nya.tar`。
- `reverse/assets/config.ini` 中的 `pz_path=ime_data_dir`、`pz_zip_name=nya.tar` 和白名单决定运行时解包位置和文件覆盖范围。
- `reverse/build.sh`、`apktool`、Android 签名工具属于 APK 重建流程，与普通 Rime 码表生成无关。

修改 APK 内置码表时，需要同时考虑 `assets/nya.tar`、解包后的 `ime_data_dir` 和 `binary-mbs/`。不要仅依据手翻 C# 文件推断完整输入法行为。

## 8. 推荐修改流程

### 修改普通编码或词条

1. 编辑 `code/1.txt`、`code/2.txt`、`code/4.txt` 或 `code/5.txt` 中的源数据。
2. 检查每行是否仍是 `文本<TAB>编码`，编码是否小写且没有意外空格。
3. 从 `code/` 执行 `bash 拼接.sh`。
4. 检查 `3_log.txt`，确认新增或变化的重码没有被意外丢弃。
5. 对比 `heom.txt`、`heom.dict.yaml`、`android/鹤仓/` 和 `ziys/` 的结果。

### 修改 Rime 行为

直接编辑 `heom.schema.yaml`，重点检查 segmentor、translator、speller、自动顶屏规则和按键绑定。码表内容变化仍应先经过 `code/拼接.sh`，不要直接手改生成的 `heom.dict.yaml`。

### 修改 Android 行为

编辑 `android/鹤仓/ime.android.ini` 或相关辅助配置。若改变了码表文件内容或文件顺序，要确认 Android 运行时使用的是文本文件还是 `binary-mbs/`，必要时重新生成对应二进制产物，再更新 APK 包内的 `nya.tar`。

## 9. 校验清单

仓库没有看到针对编码结果的自动化测试，修改后至少应做以下检查：

- `bash -n code/拼接.sh` 检查 shell 语法。
- `python3 -m py_compile code/防重.py` 检查 Python 语法。
- 从 `code/` 执行生成脚本，并确认命令无错误退出。
- 随机检查短码、四码、多重码、`ok` 查询码和 `code/5.txt` 自定义词条。
- 检查生成文件是否仍为 UTF-8、tab 分隔，且没有把日志或注释误写入码表。
- Rime 侧确认 `heom` 方案可加载、四码可顶屏、`ok` 查询可用。
- Android 侧确认明文码表、用户词库、辅助码表和二进制码表没有相互错位。

不要在没有明确需求时手工编辑 `heom.txt`、`heom.dict.yaml`、`heom_s*.txt`、`ziys/` 下的合并文件或 Android 复制产物；下一次运行 `code/拼接.sh` 会覆盖这些修改。
