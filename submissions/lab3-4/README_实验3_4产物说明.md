# 实验 3/4 产物说明

## 目录结构

- `实验3_4_地图构建与定位实验报告.tex`：实验 3/4 合并版 LaTeX 报告源文件。
- `实验3_4_地图构建与定位实验报告.pdf`：实验 3/4 合并版最终 PDF 报告，4 页 A4。
- `results/`：LaTeX 报告使用的 ASCII 文件名图片副本。
- `evidence/screenshots/`：本次重新整理的实验 3/4 截图证据，包括 Gazebo 仿真、建图过程、AMCL 粒子云收敛和实车/远程定位过程。
- `screenshots/`：实验过程截图。
- `source/launch/`：实验 3 建图、实验 4 定位相关 launch 文件。
- `source/param/`：AMCL、Hector SLAM、RF2O 等参数文件。
- `source/maps/`：实验 3 保存并供实验 4/5 复用的静态地图 `nav.pgm` 与 `nav.yaml`。
- `人工智能2302_蒋梓轩_汪翌秦_孙靖淞_实验3-4_地图构建与定位_正式提交.zip`：按指导书要求整理的实验 3/4 合并正式提交包，密码为 `robotics12`。

## 截图对应关系

- `实验3_Gazebo仿真环境.png`：Gazebo 中加载机器人和仿真环境。
- `实验3_RViz栅格地图.png`：RViz 中 `/map` 栅格地图构建结果。
- `实验4_静态地图定位显示.png`：在静态地图中显示机器人、TF、LaserScan/Map 等定位相关信息。
- `实验3_QQ过程记录.png`：聊天记录中的实验三仿真地图扫描过程记录，可作为辅助材料。
- `evidence/screenshots/lab34_gazebo_environment.png`：Gazebo 仿真场景，显示墙体、圆柱、方块障碍物和小车环境。
- `evidence/screenshots/lab34_final_sim_map.png`：仿真环境中保存后的栅格地图。
- `evidence/screenshots/lab34_hector_mapping_process.png`：Hector 建图过程中的 RViz 地图增长状态。
- `evidence/screenshots/lab34_particlecloud_initial.png` 与 `lab34_particlecloud_converged.png`：AMCL 粒子云由分散到收敛的定位过程。
- `evidence/screenshots/lab34_real_*`：实车/远程环境中的地图、LaserScan、TF 和 PoseArray 定位跟踪过程。

## 关键源码/配置

- `slam_gmapping.launch`：启动 gmapping 建图节点，配置 `base_frame`、`odom_frame`、`map_frame` 与建图参数。
- `slam_hector.launch`：启动 hector_mapping，并支持 `baseline`、`fine`、`coarse` 三种分辨率配置。
- `test_amcl.launch`：加载 `map_server`、RF2O 激光里程计和 AMCL。
- `nav01_amcl.launch`：AMCL 定位节点配置，使用 `map -> odom -> base_footprint` 坐标链。
- `nav01_rf2o.launch`：RF2O 激光里程计节点配置。

## 正式提交包口径

- 合并正式包包含 `report/实验3_4_地图构建与定位实验报告.pdf`、`code/catkin_ebot/src/ebot_bringup`、`code/catkin_ebot/src/robot_sim` 和 `evidence/`。
- `code/` 中保留建图、雷达、静态 TF、AMCL/RF2O、地图和仿真模型相关文件；未包含 `build/`、`devel/`、`.DS_Store` 或 `__pycache__` 等临时/编译产物。
- 正式提交包的 `evidence/` 中保留本次提供的截图和两个实验过程视频，便于老师需要时核对实验过程；仓库展开目录只保留截图，避免视频重复占用空间。

## 实验结果摘要

实验 3/4 合并报告完整呈现了从 Gazebo/RViz 建图、Hector 实车建图、地图保存，到 AMCL 粒子云收敛和定位跟踪的链路。最终静态地图保存为 `nav.pgm` 与 `nav.yaml`，并在该地图上完成 AMCL 定位验证，为实验 5 路径规划提供输入。
