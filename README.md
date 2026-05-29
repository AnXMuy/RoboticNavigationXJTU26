# RoboticNavigationXJTU26（Real Robot Only）

本仓库已按课程实验要求重构为**仅实车实现**（ROS1 Noetic）。

## 1. 代码范围

- 已保留：实车底盘、实车雷达、建图、定位、路径规划。
- 已移除：旧的仿真工作流与旧 guide 文档体系。
- 连接辅助工具仅保留在 `tools/`：
  - `lan_ssh_guide.sh`
  - `board_param_check.sh`

## 2. 权威指南

请直接阅读并按此执行：

- `group12_navigation_functions.html`

该文档是 cookbook 形式，包含：
- 实验2~5逐步命令
- 参数调优入口
- 常见故障定位流程
- 报告取证模板

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

后续建图/定位/导航命令请按 `group12_navigation_functions.html` 执行。
