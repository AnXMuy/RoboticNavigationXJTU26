# 实验 5 产物说明

## 目录结构

- `实验5_路径规划实验报告.tex`：与实验 2 同风格的 LaTeX 报告源文件。
- `实验5_路径规划实验报告.pdf`：由 LaTeX 报告编译得到的 PDF 报告。
- `实验5_路径规划实验报告.docx`：Word 版备份。
- `实验5_路径规划实验报告.md`：报告文本备份，便于继续修改。
- `results/`：LaTeX 报告使用的 ASCII 文件名图片副本。
- `screenshots/`：实验 5 过程截图。
- `source/launch/`：导航测试启动文件。
- `source/param/`：代价地图、局部规划器、AMCL、RF2O 和 move_base 参数文件。
- `source/maps/`：路径规划使用的静态地图文件。
- `source/reference_src/`：从导航栈源码中提取的参考文件，包括 `move_base.cpp`、全局规划、代价地图层和局部规划相关源码。
- `人工智能2302_蒋梓轩_汪翌秦_孙靖淞_实验5_路径规划_正式提交.zip`：按实验指导书“实验报告和代码打包、加密压缩”要求整理的正式提交包，密码为 `robotics12`。其中报告只放 PDF，代码按 `code/catkin_ebot/src/ebot_bringup` 结构放置导航相关 launch、param 和 map 文件。

## 截图对应关系

- `实验5_导航目标发布.png`：RViz 中发布 2D Nav Goal。
- `实验5_路径规划初始.png`：全局路径和局部路径初始规划结果。
- `实验5_全局路径与局部跟踪.png`：Gazebo 中机器人沿规划任务运动过程。
- `实验5_未知障碍物加入_Gazebo.png`：Gazebo 中加入原静态地图未知的障碍物。
- `实验5_局部代价地图更新.png`：新增障碍物被局部代价地图标记并膨胀。
- `实验5_动态避障与重规划.png`：RViz 中显示新增障碍物后的局部代价地图、路径和机器人位姿综合状态。

## 关键配置

- `costmap_common_params.yaml`：配置 `robot_radius`、`obstacle_range`、`raytrace_range`、`inflation_radius`、`observation_sources: scan`。
- `local_costmap_params.yaml`：配置 `rolling_window: true`、`update_frequency: 10.0`、局部窗口尺寸 `3.0 x 3.0 m`。
- `global_costmap_params.yaml`：配置全局坐标系 `map`、机器人坐标系 `base_footprint`，并启用静态地图。
- `base_local_planner_params.yaml`：配置局部规划器速度、加速度、采样和目标容差。
- `move_base_params.yaml`：配置规划频率、控制频率、恢复行为等。

## 实验结果摘要

实验 5 在实验 3 静态地图和实验 4 AMCL 定位基础上启动 `move_base`，实现了通过 RViz 发布目标点后的自主路径规划。新增未知障碍物后，局部代价地图能够根据 `/scan` 实时更新障碍物和膨胀区，局部规划器据此调整轨迹，实现动态避障。
