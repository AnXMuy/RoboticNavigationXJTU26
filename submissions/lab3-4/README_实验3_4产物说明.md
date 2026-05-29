# 实验 3/4 产物说明

## 目录结构

- `screenshots/`：实验过程截图。
- `source/launch/`：实验 3 建图、实验 4 定位相关 launch 文件。
- `source/param/`：AMCL、Hector SLAM、RF2O 等参数文件。
- `source/maps/`：实验 3 保存并供实验 4/5 复用的静态地图 `nav.pgm` 与 `nav.yaml`。

## 截图对应关系

- `实验3_Gazebo仿真环境.png`：Gazebo 中加载机器人和仿真环境。
- `实验3_RViz栅格地图.png`：RViz 中 `/map` 栅格地图构建结果。
- `实验4_静态地图定位显示.png`：在静态地图中显示机器人、TF、LaserScan/Map 等定位相关信息。
- `实验3_QQ过程记录.png`：聊天记录中的实验三仿真地图扫描过程记录，可作为辅助材料。

## 关键源码/配置

- `slam_gmapping.launch`：启动 gmapping 建图节点，配置 `base_frame`、`odom_frame`、`map_frame` 与建图参数。
- `slam_hector.launch`：启动 hector_mapping，并支持 `baseline`、`fine`、`coarse` 三种分辨率配置。
- `test_amcl.launch`：加载 `map_server`、RF2O 激光里程计和 AMCL。
- `nav01_amcl.launch`：AMCL 定位节点配置，使用 `map -> odom -> base_footprint` 坐标链。
- `nav01_rf2o.launch`：RF2O 激光里程计节点配置。

## 实验结果摘要

实验 3 完成了仿真环境地图构建，并保存为 `nav.pgm` 与 `nav.yaml`。实验 4 在该静态地图上启动 AMCL 定位，结合机器人 TF、激光雷达数据和里程计信息，实现机器人在 `map` 坐标系下的全局定位与运动跟踪。
