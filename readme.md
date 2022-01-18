![openSTM](openSTM.jpg)

# 简介

你好，本项目是一个旨在通过DIY来搭建一个原子级扫描隧道显微镜。

截止至2021年11月，本项目已经搭建起了不稳定的隧穿电流。

# 开源文件结构介绍

由于本项目尚未完成，故在此仅对已开源的文件进行简单介绍，暂不详细介绍使用方法。

- 3DModels

  该目录包括了使用SolidWorks绘制的扫描隧道显微镜模型。

- ArduinoProject

  该目录包括了使用[Arduino](https://www.arduino.cc/)（[PlatformIO](https://platformio.org/)）完成的工程。

  - DAC_CONTROLLER

    该目录包括了以ESP32主控制器，用于控制DAC的工程（使用了LVGL图形库）。

  - ViberationDetector

    该目录包括了用于机械振动频率分析的小工具。（使用了MPU6050及FFT库）。

- Documents

  该目录下包括了在开发过程中参考的论文、数据手册。（如涉及版权问题，请提交Issue删除）

- PCBs

  该目录下包括了DAC控制板、前级放大器、DAC板的立创EDA工程。

- PythonScripts

  该目录下包括了Python脚本工具，目前仅有用于数干涉条纹的工具。

- Simulation

  该目录放置仿真文件，目前仅有ADP5070基于SpiceSimulation的仿真。

# 联系我

如果你也想制作一个STM显微镜，或者对我有什么建议的话，可以在此页面提交Issue。

# 开发记录

- 2021/11

  不稳定隧穿

- 2022/1/11

  开源页面提交

- 2022/1/18

  减震台下加装了<网球>，减震效果拔群

