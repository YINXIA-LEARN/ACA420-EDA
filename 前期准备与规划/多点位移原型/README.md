# 四点位移原型的复现与交接

本目录保存可独立运行的两个实验及合成样例。系统设计与分工见[实施方案](../实施方案.md)。

**Python 实验**：在本目录打开 PowerShell，用可用的 Python 3 创建虚拟环境（本次复验使用 3.13）。若系统用 `py` 选择解释器，可把首行的 `python` 换成 `py -3`。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install numpy matplotlib opencv-python-headless
.\.venv\Scripts\python run_model.py --demo --output "$env:TEMP/aca420-demo"
```

脚本生成 150 帧人工图像，每帧记录 R、P1、P2、P3。P2 在编号 48～58 的帧被遮挡，预期连续 11 帧无效。 [样例 CSV](output/measurements.csv) 与[位移图](output/displacement.png)使用人工设定的 0.10 mm/px，适合核对去漂移和失锁逻辑。本次复跑的 600 行记录与样例逐字段一致。`--image` 只按演示坐标检查一张图片，实拍输入需配置对应 ROI 和标定系数。

**RTL 实验**：在已配置 ModelSim 命令的终端，从本目录运行下列命令。测试给出两个命中像素、一个低灰度像素和一个 ROI 外像素，帧切换时预期 `count=2, sum_x=30, sum_y=70`。

```powershell
vlib work
vlog -sv rtl/roi_accumulator.v rtl/tb_roi_accumulator.v
vsim -c work.tb_roi_accumulator -do "run -all; quit -f"
```

本次 ModelSim 2020.1 输出 `PASS roi_accumulator`。这个模块只输出单个区域的整数和。接入相机前需对齐三处语义：RTL 采用 `gray >= threshold`，Python 的 OpenCV 二值化采用严格大于；Python 会随上帧坐标移动窗口，现行硬件起步方案固定窗口；RTL 在 `frame_start` 输出上一帧并清零，该拍不计像素。B/C 先用相同 ROI、等于阈值的像素及帧首/帧末向量验证，再将软件输出作为 RTL 对照。
