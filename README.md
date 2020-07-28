<!-- PROJECT -->

  <h3 align="center">PokemonHelper</h3>

  <p align="center">
    AFK script implemented on GBA monitor platform for Pokémon Emerald and derivative versions



## About The Project

<p align="center"><stong>
    This repository is for own use, therefore, it is not considered to expand the support of other language versions or operating systems
</strong></p>



此项目的念头出自本人苦苦挣扎于《漆黑的魅影》的蛋闪之时。由于蛋闪之出产率远低于可操作的6v，为蛋闪而奔波的日子无比枯燥且乏味。此时在贴吧之中看到一位老兄开发的基于手机按键精灵的自动蛋闪脚本，并的确借助其成功实现了人生中的第一枚闪蛋蛋。（即便非手动没有灵魂，但真香）

蛋闪脚本的成功激发了自动化的念头，尤其是6v的自动化。毕竟在手动操作之下，虽然有红线机制的加入，手动育种的工作仍需要许多代的培育。而一旦可以自动化，利用6v父本便可以实现第一代培养5v母本，第二代便出产6v的两代流。但这需要个体值的识别，此外一些移动换位的操作也是相当繁琐的。这样的程序放在按键精灵脚本上恐怕成本（学习成本，调试成本）都将非常大。因此我选择了使用Python脚本来实现。

`6v脚本`(个体值查询脚本):

​	个体值的识别本质上是数字图像识别，识别的工作由pytessearct实现；而截图在linux下因为没有较合适的包，我使用了于stackoverflow上找到的基于Xlib的c语言截图函数包，并加载在了python下；至于按键的操作，使用的是pyautogui，来模拟鼠标点击（因为采用了投屏功能，若使用PC端GBA则可以尝试换用成键盘敲击）

​	初始条件：朝上面对孵蛋老爷爷

`蛋闪脚本`：

​	初始条件：在蛋即将孵化的"哼"的场景

`位置确定脚本`:

​	无论是截图还是按键(模拟鼠标点击)都需要得知位置区域或者虚拟按键的位置，因此位置确定脚本正是用于辅助位置确定的。

### Requirement 

* pytesseract==0.3.4
* PyAutoGUI==0.9.50
* Pillow==7.2.0




