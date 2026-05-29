# RoboticNavigationXJTU26

西安交通大学移动机器人导航课程实验仓库（ROS1 Noetic）。

## 1. 仓库结构

- `src/ebot_bringup/`：统一启动入口与参数配置。
- `src/ebot_base/turn_on_wheeltec_robot/`：底盘串口驱动。
- `src/ebot_sensors/ydlidar_ros_driver/`：YDLidar 驱动。
- `src/ebot_navigation/`：AMCL、move_base、costmap、规划器等导航包。
- `docs/`：实验指导书与执行指南。
- `tools/`：构建档位与状态检查脚本。

## 2. 环境准备

```bash
cd /Users/zixuan/XJTU/RoboticNavigation
eval "$(conda shell.zsh hook)"
conda activate ros1_noetic
export ROS_PACKAGE_PATH="$PWD/src:${ROS_PACKAGE_PATH:-}"
```

## 3. 编译（实车）

```bash
./tools/use_real_profile.sh
./tools/show_build_profile.sh
catkin_make
source devel/setup.bash
```

## 4. 关键运行入口

### 4.1 实验2：实车键控

```bash
roslaunch ebot_bringup bringup.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

### 4.2 实验3：实车建图（Hector）

```bash
roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup my_lidar.launch
roslaunch ebot_bringup slam_hector.launch resolution_profile:=baseline
```

### 4.3 实验4：实车定位

```bash
roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup my_lidar.launch
roslaunch ebot_bringup test_amcl.launch map:=nav.yaml amcl_profile:=baseline
```

### 4.4 实验5：实车路径规划与避障

```bash
roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup my_lidar.launch
roslaunch ebot_bringup test_nav.launch map:=nav.yaml amcl_profile:=baseline
```

## 5. 参数入口

- `resolution_profile:=baseline|fine|coarse`（`slam_hector.launch`）
- `amcl_profile:=baseline|fast|robust`（`test_amcl.launch` / `test_nav.launch`）
- `global_planner:=navfn/NavfnROS|global_planner/GlobalPlanner`
- `local_planner:=base_local_planner/TrajectoryPlannerROS|dwa_local_planner/DWAPlannerROS`
- `costmap_profile_file:=<yaml_path>`（覆盖默认 `costmap_common_real.yaml`）

## 6. 文档入口

- 运行说明：`docs/运行说明_实机与仿真.md`（已更新为实车版）
- 总览索引：`docs/guides/00_实验总览_执行与报告索引.md`
- 分实验指南：`docs/guides/01~05_*.md`

## 7. 常见问题

- `/scan` 不更新：检查串口路径、设备权限、`ydlidar_real.yaml` 参数。
- `amcl` 无法收敛：检查地图坐标系与 `rf2o_laser_odometry` 是否发布稳定里程计。
- `move_base` 无法下发速度：检查 TF 链与局部/全局代价地图参数加载是否成功。
