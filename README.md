# RoboticNavigationXJTU26

西安交通大学移动机器人导航课程实验仓库（ROS1 Noetic）。

本仓库用于统一管理实验 1~5 的代码与文档，覆盖以下能力：
- ROS 基础通信（话题、服务）
- 键控机器人运动与 TF 理解
- 地图构建（Gmapping / Hector）
- 基于 AMCL 的定位
- 基于 `move_base` 的路径规划与避障

仓库同时支持：
- `mode:=real` 实车链路
- `mode:=sim` 仿真链路

并通过构建档位脚本将仿真与实车依赖解耦，方便在无实车环境的 PC 上单独完成仿真实验。

## 1. 仓库结构

- `src/`
  - `ebot_bringup/`：统一启动入口（launch）与参数配置（config）
  - `ebot_navigation/`：导航相关包（`amcl`、`move_base`、`costmap_2d` 等）
  - `robot_sim/`：Gazebo 仿真模型与世界文件
  - `vehicle_sim/`：RViz 轻量仿真（实验2）
  - `ebot_base/`、`ebot_sensors/`：实车底盘与雷达驱动
- `docs/`
  - 实验指导书 PDF
  - `guides/`：按实验顺序整理的执行与报告指南
- `tools/`
  - 构建档位切换脚本（仿真/实车）
  - 运维辅助脚本

## 2. 环境要求

推荐课程标准环境：
- Ubuntu 20.04
- ROS Noetic

本地也可使用 Conda 的 ROS1 环境（如 `ros1_noetic`），但在非标准平台上（例如 macOS + Conda）部分 Gazebo 传感器插件可能存在兼容差异。

## 3. 快速开始

```bash
cd /Users/zixuan/XJTU/RoboticNavigation
eval "$(conda shell.zsh hook)"
conda activate ros1_noetic
export ROS_PACKAGE_PATH="$PWD/src:${ROS_PACKAGE_PATH:-}"
```

### 3.1 仿真专用构建（推荐无实车时）

```bash
./tools/use_sim_profile.sh
./tools/show_build_profile.sh
catkin_make
source devel/setup.bash
```

### 3.2 实车构建

```bash
./tools/use_real_profile.sh
./tools/show_build_profile.sh
catkin_make
source devel/setup.bash
```

## 4. 关键运行入口

### 实验2：键控模型（RViz）

```bash
roslaunch vehicle_sim vehicle_sim_rviz.launch
```

### 实验3：地图构建

仿真 Gmapping：
```bash
roslaunch ebot_bringup bringup.launch mode:=sim
roslaunch ebot_bringup slam_gmapping.launch
```

实机 Hector：
```bash
roslaunch ebot_bringup bringup.launch mode:=real
roslaunch ebot_bringup my_lidar.launch mode:=real
roslaunch ebot_bringup slam_hector.launch mode:=real
```

### 实验4：定位

```bash
roslaunch ebot_bringup test_amcl.launch mode:=sim map:=nav.yaml amcl_profile:=baseline
```

### 实验5：路径规划

```bash
roslaunch ebot_bringup test_nav.launch mode:=sim map:=nav.yaml
```

## 5. 进阶实验参数入口

- Hector 分辨率对比：
  - `resolution_profile:=baseline|fine|coarse`
- AMCL 参数档位：
  - `amcl_profile:=baseline|fast|robust`
- 规划器切换：
  - `global_planner:=navfn/NavfnROS|global_planner/GlobalPlanner`
  - `local_planner:=base_local_planner/TrajectoryPlannerROS|dwa_local_planner/DWAPlannerROS`
- 代价地图对比：
  - `costmap_profile_file:=<path_to_yaml>`

## 6. 实验执行指南（建议按顺序）

位于 `docs/guides/`：
- `00_实验总览_执行与报告索引.md`
- `01_实验1_ROS通信机制_执行与报告指南.md`
- `02_实验2_键控机器人运动_执行与报告指南.md`
- `03_实验3_地图构建_执行与报告指南.md`
- `04_实验4_定位实验_执行与报告指南.md`
- `05_实验5_路径规划_执行与报告指南.md`

每份指南均包含：
- 逐步命令
- 预期结果与验收点
- 报告取证清单
- 对应进阶要求的可执行步骤

## 7. 常见问题

- `map_server` / `amcl` / `move_base` 找不到可执行：
  - 检查 ROS 安装是否完整，确认已 `source devel/setup.bash`。
- 仿真中无 `/scan`：
  - 先检查 Gazebo 内部激光 topic；若 ROS 侧仍无，优先在 Ubuntu20.04 + Noetic 复现。
- 地图加载失败：
  - 检查 `src/ebot_bringup/maps/nav.yaml` 的 `image` 路径是否正确。

## 8. 维护说明

仓库维护规范见：
- `Maintain.md`
