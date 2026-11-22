# ACA420-EDA · 多测点结构位移与低频振动测量

## 第一次参与：Fork、分支、PR

三人共用 [YINXIA-LEARN/ACA420-EDA](https://github.com/YINXIA-LEARN/ACA420-EDA) 作为主仓库。`main` 保存全队认可的版本。**Fork** 是自己账号下的仓库副本，**分支**用来独立完成一项任务，**PR（Pull Request）** 是请队友审查并把改动合回主仓库的请求。

1. **领一个任务。** 登录 GitHub，在主仓库的 Issues 新建或认领一项工作，写清负责人、交付物和验收方法。例如“B：遮住参考点时，所有校正位移均标为无效”。评论认领即可。
2. **第一次配置。** 队员在主仓库页面点 **Fork → Create fork**。安装 Git 后打开 PowerShell，把下面的 `YOUR-NAME` 换成自己的 GitHub 用户名，在准备存放项目的目录运行。已有本地仓库的成员先用 `git remote -v` 核对远程地址，避免重复克隆。

   ```powershell
   git clone https://github.com/YOUR-NAME/ACA420-EDA.git
   cd ACA420-EDA
   git remote add upstream https://github.com/YINXIA-LEARN/ACA420-EDA.git
   git remote -v
   ```

   `origin` 指自己的 Fork，`upstream` 指主仓库。首次提交如提示身份未设置，在此目录运行 `git config user.name "你的名字"` 和 `git config user.email "你的 GitHub 提交邮箱"`。主仓库所有者可以直接在自己的克隆中新建任务分支、推送并发 PR；以下同步命令中的 `upstream` 对所有者可换成指向主仓库的 `origin`。
3. **每次从最新主线开分支。** 先确认 `git status` 干净。下面用补充采集接口说明举例，每个任务换一个分支名。

   ```powershell
   git switch main
   git fetch upstream
   git merge --ff-only upstream/main
   git push origin main
   git switch -c docs/camera-interface
   ```

4. **修改、检查、推送。** 做完后运行与改动相关的验证。以下示例只暂存本次改动的方案文件；改其他文件时换成相应路径。首次推送按 Git 提示完成 GitHub 登录。

   ```powershell
   git status --short
   git diff
   git add -- "前期准备与规划/实施方案.md"
   git diff --cached
   git commit -m "说明摄像头帧起点与首个有效像素的关系"
   git push -u origin docs/camera-interface
   ```

5. **发 PR、审查、合并。** 在 GitHub 点 **Compare & pull request**；目标选 `YINXIA-LEARN/ACA420-EDA:main`，来源选自己 Fork 的任务分支。说明“改了什么、怎么验证、哪些还待上板”，附 Issue 编号或 `Closes #编号`。另一名队员检查 Files changed 和证据；作者按意见在**同一分支**提交并推送，原 PR 会更新。审查通过后由有权限的成员合并。回到第 3 步同步，再领下一项。如出现冲突，先在任务分支与修改同一文件的队友核对，两人确认结果后再合并。[GitHub 官方 PR 图解](https://docs.github.com/zh/pull-requests/how-tos/create-pull-requests/creating-a-pull-request-from-a-fork)

## 作品和进度

我们用小梅哥 ACA420-EDA（安路 EG4S20BG256）做一台桌面悬臂梁测量终端。目标是让一台相机同时看见固定参考点和多个运动点，FPGA 逐帧算出位移，在 VGA 画面叠加测点状态，串口留下可与量具核对的数据。当相机轻微平移或标记被遮住，观察者可以直接比较校正效果和失锁状态。

目前可复现的是 **Python 合成实验**和**单 ROI 累加器仿真**。前者在 150 帧上生成 600 条测点记录，后者已通过现有四个像素输入的测试。整机相机采集、标定精度、频段和资源利用率仍待本板实测。参赛资格由团队按当届选题确认。

| 你要做什么 | 从这里开始 |
|---|---|
| 看功能取舍、15 日排期、交接接口和验收条件 | [现行实施方案](前期准备与规划/实施方案.md) |
| 在电脑复现算法、对照 CSV、跑单 ROI 仿真 | [多点位移原型](前期准备与规划/多点位移原型/README.md) |
| 找原理图某一页、管脚、器件手册或章节工程 | [资料导航](AGENTS.md)；首次认板可读[板卡笔记](<资料/ACA420-EDA 板卡笔记.md>) |
| 找旧平台方案及调研出处 | [废案归档索引](前期准备与规划/废案/README.md) |

## 三个人怎样接起来

| 分工 | 第一个可交付结果 | 谁来复核 |
|---|---|---|
| A · 板卡、视频与 TD 工程 | 复现第 36 章，交一帧真实数据、像素时序、相机设置和显示画面 | B 根据接口接入 ROI，C 核对标记是否清晰 |
| B · 测量 RTL 与输出 | 在同帧输出参考点和两个动点的统计量、有效位及帧号，附遮挡向量 | C 用 Python 核对数值，A 核对跨时钟域与时序 |
| C · 工位、模型与实验 | 搭好独立支架、同平面标尺，记录真实标定和误差，整理复演步骤 | A/B 按记录独立重复一次 |

每个 Issue 留下当前提交号、阻塞项和下一次交接对象。PR 中把**合成数据、RTL 仿真、板上实测**分别标记。提交自研源码、约束、测试和小型可复核样本；TD 构建缓存、ModelSim 工作库、整段实验录像留在本地或在证据说明中给出位置。厂商资料保持原目录和作者标识。本地完整版另有 TD、ModelSim 等安装程序和许可证，GitHub 克隆只包含已跟踪的资料。
