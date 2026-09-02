// 手翻自 libaot-PangIme.Maui.dll.so:0x44e0+pang_so.asm + smali/PangIME/Android/InputService.smali:13
// 原C# (PangIme.Maui, Full AOT stripped) -> 伪还原，仅保留与 ime.android.ini:14354 的数据链一致性
// 逻辑：ini驱动，txt词库->binary-mbs 索引，xpa/xp 皮肤
using Android.InputMethodServices;
using Android.Views;

namespace PangIme.Maui {
  // 对应 smali: PangIME.Android.InputService -> TypeManager.Activate("PangIme.Maui.InputService, PangIme.Maui")
  public class InputService : InputMethodService {
    // mono_aot_file_info v186 0xBA, GOT 0x2677c0, trampoline fcn.001a2530...
    // 原native: n_onCreate / n_onCreateInputView / n_onStartInputView 等均转GOT
    public override void OnCreate() {
      // 解 assets/nya.tar -> ime_data_dir (config.ini: pz_path/pz_always_extract)
      // if (!Exists(ime_data_dir) || pz_always_extract==1) ExtractTar("nya.tar", pz_path, pz_white_list)
      base.OnCreate();
    }
    public override View OnCreateInputView() {
      // 读 ime_data_dir/鹤仓/ime.android.ini -> file00=heom.txt (2860203)
      // workmode=0 内存查 mb.main.data.bin/mb.main.index.bin
      // usedassisttype/extendtype 决定候选，push/ding/empty 控制上屏
      return base.OnCreateInputView();
    }
    public override View OnCreateCandidatesView() {
      // 渲染 FloatCandiView / KeyBoardCustomView，读 skins/*.xpa (zip aj.ogg/preview)
      return base.OnCreateCandidatesView();
    }
    public override void OnStartInputView(Android.Views.InputMethods.EditorInfo info, bool restarting) {
      base.OnStartInputView(info, restarting);
    }
  }
}
