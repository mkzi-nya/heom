只是用来存一下代码，防止弄丢罢了，反正除了我应该也没人会用这种东西  
  
作者qq[2450382239](https://qm.qq.com/q/UfEfmy7MEE)  
可到[https://mkzi-nya.github.io/IME-Converter-web/index.html](https://mkzi-nya.github.io/IME-Converter-web/index.html)试用  
是以鹤形为基础将形码部分改成仓颉改的输入法  
比如鹤：鹤=hedn，仓：鹤=ogpym，加起来变成heom  
code文件夹里是源文件，结构如下  
- 0.txt rime词库开头代码  
- 1.txt 大多为原鹤形重排  
- 2.txt 按规则扩展的单字，1和2加起来包含所有unicode中有读音的汉字  
- 3.txt是解决因为扩展出现的重码的，使他不超过3选，日常基本不可能用到  
- 4.txt是ok+仓颉码（替代原ok拼字）  
- 5.txt是我自己的码表  
- yaml是rime的文件
带\_s的是排序后的，带\_s\_1的是颠倒tab符前后的顺序  
apk装上能直接用，从小胖改的  
