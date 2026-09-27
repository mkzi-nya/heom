// Frida hook 兜底：无需改so，运行时改逻辑，效果与重编一致
// frida -U -l frida_hook.js -f nya.IME
Java.perform(function(){
  var InputService = Java.use("PangIME.Android.InputService");
  InputService["n_onCreate"].implementation = function(){
    console.log("[hook] InputService.n_onCreate");
    // 在此改 config.ini / heom.txt 路径：重定向到 /data/data/nya.IME/files/ime_data_dir
    return this["n_onCreate"].apply(this, arguments);
  };
  InputService["n_onStartInputView"].implementation = function(info, restarting){
    console.log("[hook] onStartInputView", info);
    // 实现双检索改写：改 usedassisttype
    return this["n_onStartInputView"].apply(this, arguments);
  };
  // 如果要patch so的候选：Interceptor.attach(Module.findExportByName("libaot-PangIme.Maui.dll.so","mono_aot_file_info"),...)
  var base = Module.findBaseAddress("libaot-PangIme.Maui.dll.so");
  console.log("[hook] so base", base);
  // 例子：hook GOT 0x2677c0 上的函数
  // Interceptor.attach(base.add(0x44e0), {onEnter: function(args){console.log("enter 0x44e0",args[0])}})
});
