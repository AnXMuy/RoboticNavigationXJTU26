# RoboticNavigationXJTU26（Real Robot Only）

本仓库已按课程实验要求重构为**仅实车实现**（ROS1 Noetic）。

## 1. 代码范围

- 已保留：实车底盘、实车雷达、建图、定位、路径规划。
- 已移除：旧的仿真工作流与旧 guide 文档体系。
- 连接辅助工具仅保留在 `tools/`：
  - `lan_ssh_guide.sh`
  - `board_param_check.sh`

## 2. Cookbook 文档入口

请按下面顺序阅读并执行：

- 总索引：`group12_navigation_functions.html`
- 实验2：`group12_exp02_teleop.html`
- 实验3：`group12_exp03_mapping.html`
- 实验4：`group12_exp04_localization.html`
- 实验5：`group12_exp05_navigation.html`

每个实验是独立 HTML，包含：
- 明确的终端分工
- 每一步命令与操作动作
- 验收标准
- 常见故障排查
- 报告记录模板

## 3. PDF 与 demo 依据

- 指导书：`docs/实验指导书-实验2~5.pdf`
- 源码来源：`demo/demo02_teleop.zip`、`demo/demo03_mapping.zip`、`demo/demo04_localization.zip`、`demo/demo05_navigation.zip`

## 4. 快速入口（只列主链路）

```bash
cd /Users/zixuan/XJTU/RoboticNavigation
eval "$(conda shell.zsh hook)"
conda activate ros1_noetic
export ROS_PACKAGE_PATH="$PWD/src:${ROS_PACKAGE_PATH:-}"
catkin_make
source devel/setup.bash

roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup my_lidar.launch
```

后续建图/定位/导航命令请按对应实验 HTML 页面执行。
