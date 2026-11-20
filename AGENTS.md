# ACA420-EDA 资料导航

目标板为小梅哥 ACA420-EDA，FPGA 为安路 EG4S20BG256。了解整板布局、外设和已核对的接线差异，直接读[板卡笔记](<资料/ACA420-EDA 板卡笔记.md>)。处理具体任务时，从下表定位文件即可。

**路径约定**：下表路径相对于厂商资料根目录 `资料/小梅哥ACA420-EDA 国产安路FPGA学习板开发板资料/`。章节号对应同一本教材，例程名对应同一章。

| 要查的问题 | 优先打开 | 在哪里找答案 |
|---|---|---|
| 引脚绑定、时钟、GPIO、串口收发方向 | `04_引脚功能信息/安路EG4S20管脚分配表.xlsx` | 查 Sheet1 的 A～C 列（功能、信号、FPGA 管脚）。核对具体例程的端口名或复位键，再看该工程的 `.adc`。 |
| 板载外设接线、电平、排针脚序 | `06_原理图&PCB/ACA420-EDA.pdf` | 第 2 页 USB 供电、串口和 JTAG；第 3 页 LCD/VGA；第 4 页 LED、开关和按键；第 5 页数码管；第 6 页 RTC、EEPROM、ADC/DAC、温度、蜂鸣器和红外；第 7 页 GPIO；第 8 页音频。 |
| 核心板电路、配置 Flash、供电或封装 | `06_原理图&PCB/ACA420-CORE.pdf` | 第 3 页查配置接口和 Flash。画 PCB 时取同目录的 `ACA420-CORE封装.zip`。 |
| 开发环境、实验原理、仿真或下载步骤 | `01_教材文档/01_【教材文档】ACA420国产安路FPGA逻辑教程V1.1.pdf` | 安装 TD、下载器驱动、配置 ModelSim 看第 1 章；首次完整上板流程看第 2 章。其他实验按下表章号跳转。 |
| 实验源码、顶层模块、管脚约束 | `02_设计实例/` | 只打开下表命中的 RAR。`.al` 列出工程源文件及顶层，`.v` 是 Verilog，`.adc` 是管脚约束。第 1、35 章的压缩包只有空目录，内容在教材。 |
| 芯片寄存器或电气时序 | `07_器件手册/` | 按器件取文件，例如 `EEPROM/24LC64.pdf`、`ES8388.pdf`、`EM638325_Rev-3.2.pdf`、`GM1302.pdf`、`DS18B20.pdf`。板载 ADC 在图纸上写 XL549，配套手册文件名为 `TLC549.PDF`。 |
| 工具安装包和驱动 | `05_驱动和常用软件/` | 本地 TD 安装包在该目录，ModelSim 在 `Modelsim-SE-10.6d/`，串口驱动在 `小工具和小软件/CH343SER.EXE`。公开仓库忽略安装程序和许可证。 |
| 摄像头模块引脚、规格 | `09_套餐配套模块资料/摄像头/ACM5640-V5/UserGuide/ACM5640-V5型500W高清摄像头模块用户手册.pdf` | 芯片寄存器查相邻的 `Datasheet/`。本板工程取第 36、37 章；模块目录下的 Demos 含其他板型。 |
| TFT 模组接口、背板和触控 | `09_套餐配套模块资料/显示屏/4.3寸5寸800x480高清电容触摸屏/` | `用户手册/` 查接口，`背板原理图/` 按屏尺寸选图，`触摸液晶屏模组厂家规格书/` 按 4.3 寸 GT9147 或 5 寸 GT911 查触控芯片；显示例程见第 27、37 章。 |

## 按实验找源码

下表每个名称都是 `02_设计实例/` 下的文件名，补上 `.rar` 即可打开。名称开头的数字就是教材章号。

| 任务关键词 | 例程文件名（省略 .rar） |
|---|---|
| 拨码译码、计数闪灯 | `ch2_decoder3_8`、`ch3_bin_counter` |
| UART 发送、接收、控制 LED、状态机、串口回环 | `ch4_uart_tx`、`ch5_uart_rx`、`ch6_uart_rx_ctrl_led`、`ch7_fsm_hello`、`ch8_uart_loopback` |
| 独立按键消抖、按键计数、八位数码管 | `ch9_key_filter`、`ch10_key_led`、`ch11_hex8` |
| PLL、ROM、RAM、串口与 RAM、FIFO | `ch12_pll`、`ch13_rom`、`ch14_ram`、`ch15_simple_ram_system`、`ch16_fifo` |
| 外接高速 DAC 波形发生器、PWM 蜂鸣器、音乐 | `ch17_DDS_AD9767`、`ch18_pwm_gen`、`ch19_music_gen` |
| 4×4 矩阵键盘、NEC 红外遥控 | `ch20_keyboard_4x4`、`ch21_HT6221` |
| 板载 DAC、ADC、数字电压表 | `ch22_dac5311`、`ch23_TLC549`、`ch24_Dig_Volt` |
| VGA 时序、通用 VGA 控制器、TFT 驱动 | `ch25_VGA_CTRL`、`ch26_General_VGA_CTRL`、`ch27_TFT_CTRL` |
| VGA 显示图片、字符、动态字符 | `ch28_rom_image_vga`、`ch29_rom_char_vga`、`ch30_dync_char_vga` |
| I²C 控制器、串口读写 EEPROM、音频回环 | `ch31_i2c_control`、`ch32_uart_to_eeprom`、`ch33_ES8388_Loop_Back` |
| SDRAM 控制器、OV5640 采集到 VGA 或 TFT | `ch34_Sdram_Control`、`ch36_ov5640_sdram_vga`、`ch37_ov5640_sdram_tft`。摄像头基础见教材第 35 章。 |
