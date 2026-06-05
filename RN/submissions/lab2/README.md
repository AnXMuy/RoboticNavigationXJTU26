# 实验 2 键控机器人运动提交说明

本目录按实验指导书整理了报告和仿真代码。

## 正式提交包

- `人工智能2302_蒋梓轩_汪翌秦_孙靖淞_实验2_键控机器人运动_正式提交.zip`：按指导书“实验报告和代码打包、加密压缩”要求整理的正式提交包，密码为 `robotics12`。

正式提交包只包含：

- `report/实验2_键控机器人运动实验报告.pdf`
- `code/catkin_ebot_sim/`

包内未包含 `build/`、`devel/`、`.DS_Store` 或 `__pycache__` 等临时/编译产物。

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
