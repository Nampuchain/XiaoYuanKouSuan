# XiaoYuanKouSuan

小猿口算炸鱼脚本。

OCR 思路，调参时意外卡上 bug ，0.25秒/题是基操，最快可实现 0.11秒/题。

## 目录

- [战绩](#战绩)
- [来源](#来源)
- [环境](#环境)
- [操作步骤](#操作步骤)
- [碎碎念](#碎碎念)

## 战绩

![](img/1.jpg)

![](img/2.jpg)

![](img/5.jpg)

## 来源

本来抱着学习的目的，自己实现一下 OCR 思路的答题脚本，结果在调 pyautogui 画答案的那个长度参数时，意外出现了 bug ，只答了第一题之后，直接跳转到胜利了。

思路：截屏 → OCR 识别 → 判定 → 绘制答案。

## 环境

- Python3

- 安卓模拟器，分辨率调成 1080x1920。固定在电脑屏幕左上方，边角重合。

  也可以自行修改代码第 21 行 region 的参数，确保能裁剪到题目区域。such as：

  ![](img/4.jpg)

- `pip install -r requirements.txt` 安装依赖，然后就可以开心地炸鱼了。

## 操作步骤

第一步：运行脚本；

第二步：看到控制台输出四个“取得数字”的内容非 `0 0` 的时候，win+D 切换到桌面，手动结束程序。

​				why? 本机的测试环境太捞了，低配轻薄本。代码中有自动结束程序的机制，但是本机带不动那么快				速度的模拟器步骤，会直接卡死。连打开模拟器运行小猿口算都卡卡的了，何况这个。编写代码的过程				中，已重启无数次，甚至有几次直接卡死机了，已落泪😭。如果是性能更好的电脑，应该是没问题的。				没测过，逃~

## 碎碎念

声明：仅供学习，无任何恶意。

个人认为 OCR 思路是最普适的，抓包思路受限太多。一麻烦，要配合抓包工具使用；二如果数据包加密并且破不了，那就 gg 了；三太被动，服务器那边制裁一下就要改进。

OCR 思路可以优化的地方很多：

1. 设备性能。
2. OCR 识别精度。本程序中只加了一些经常识别错误的特判，没有针对 OCR 本身。
3. 处理算法。应该还是存在很多改进思路的，就本人而言，改进的地方如下：
   - 截屏和绘制答案，原来是利用 adb 在模拟器里操作，后改为用 pyautogui 在电脑屏幕操作。
   - 使用 pyautogui 移动坐标太慢，改为用 windll 。

求解：为什么答了一题就自动跳转到胜利了？如图：

![](img/3.jpg)

该 bug 源于代码第 82 行 `for i in range(20)` 对 range 里的数字进行调整测试，改为 10 就不行了，求解。