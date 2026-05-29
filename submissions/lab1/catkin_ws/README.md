# Lesson 1 — ROS 通信机制实验代码

按实验报告复现的 catkin 工作空间，纯 Python 实现。

## 目录结构

```
catkin_ws/src/
├── plumbing_pub_sub/         # 话题通信
│   ├── scripts/{talker,listener}.py
│   └── launch/pubsub.launch
├── plumbing_server_client/   # 服务通信
│   ├── srv/AddInts.srv
│   ├── scripts/addints_{server,client}.py
│   └── launch/addints.launch
└── turtle_control/           # 小乌龟圆周运动
    ├── scripts/{circle_pub,pose_sub}.py
    └── launch/turtle_full.launch
```

## 编译

```bash
cd catkin_ws
catkin_make -DCMAKE_POLICY_VERSION_MINIMUM=3.5   # macOS RoboStack（cmake 4.x）需要
# Ubuntu 真机直接 catkin_make 即可

source devel/setup.zsh    # zsh
# source devel/setup.bash # bash
```

## 运行

```bash
# 1. 小乌龟圆周运动 + 位姿订阅
roslaunch turtle_control turtle_full.launch

# 2. 话题通信
roslaunch plumbing_pub_sub pubsub.launch

# 3. 服务通信
rosrun plumbing_server_client addints_server.py            # 终端 A
rosrun plumbing_server_client addints_client.py 10 20       # 终端 B
```

## 关键参数

| 项 | 值 |
|---|---|
| `chatter` 发布频率 | 10 Hz，`std_msgs/String` |
| `cmd_vel` 速度 | linear.x=1.0, angular.z=0.5 |
| `AddInts` 服务 | `int32 num1, num2 → int32 sum`，负数返回默认响应 |
