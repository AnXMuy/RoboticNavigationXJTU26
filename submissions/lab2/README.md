# 实验 2 键控机器人运动提交说明

本目录按实验指导书整理了报告和仿真代码。

## 仿真运行

```bash
cd catkin_ebot_sim
catkin_make
source devel/setup.bash
roslaunch vehicle_sim vehicle_sim_rviz.launch
```

另开一个终端启动键盘控制：

```bash
source catkin_ebot_sim/devel/setup.bash
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

## 检查要求

```bash
rostopic info /cmd_vel
rostopic echo /odom
rosrun rqt_tf_tree rqt_tf_tree
```

`vehicle_sim.py` 订阅 `/cmd_vel`，发布 `/odom`，并广播 `odom -> base_footprint` 的动态 TF。
