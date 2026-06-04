# 实验 6 产物说明

## 目录结构

- `实验6_控制实验报告.md`：实验 6 报告源文件。
- `实验6_控制实验报告.pdf`：最终 PDF 报告。
- `实验6_控制实验报告.docx`：Word 版本报告，便于二次编辑。
- `build_lab6_report.py`：从 Markdown 生成轨迹图、PDF 与 DOCX 的脚本。
- `results/pid_tracking_curve.png`：PID 圆形路径跟踪示意图。
- `source/`：实验 6 相关代码快照，包含 `pid_controller`、`styx_msgs`、`vehicle_sim` 以及 `turn_on_wheeltec_robot` 中的阿克曼里程计修改。
- `人工智能2302_蒋梓轩_汪翌秦_孙靖淞_实验6_控制实验_正式提交.zip`：正式提交包，密码为 `robotics12`。

## 主要代码入口

- `source/pid_controller/launch/simple_follow.launch`：PID 循迹仿真启动文件，默认使用圆形路径。
- `source/pid_controller/waypoints/`：直线、圆形、方形、心形等参考路径 CSV。
- `source/pid_controller/src/ebotController.cpp`：PID 控制器，支持 `/base_waypoints` 与 `/move_base/GlobalPlanner/plan` 两种参考线输入。
- `source/vehicle_sim/scripts/vehicle_sim.py`：仿真车自行车模型里程计。
- `source/turn_on_wheeltec_robot/src/wheeltec_robot.cpp`：实车底盘阿克曼里程计积分与 `/odom` 发布逻辑。

## 复现实验命令

```bash
catkin_make
source devel/setup.bash
roslaunch pid_controller simple_follow.launch
```

切换路径示例：

```bash
roslaunch pid_controller simple_follow.launch \
  path_file:=$(rospack find pid_controller)/waypoints/heart.csv \
  kp:=0.85 ki:=0.02 kd:=0.18 target_speed:=0.45
```

正式提交包只包含 `report/`、`code/` 和 `results/`，未包含 `build/`、`devel/`、`.DS_Store` 或 `__pycache__` 等临时产物。
