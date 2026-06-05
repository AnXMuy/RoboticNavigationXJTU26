# 实验一：ROS 通信机制 — 安装与运行说明

## 一、环境要求

- 操作系统：Ubuntu 20.04 LTS（Focal Fossa）
- ROS：Noetic Ninjemys
- Python：3.8（Ubuntu 20.04 默认）

## 二、安装 ROS Noetic

完整官方步骤见 https://wiki.ros.org/noetic/Installation/Ubuntu 。下面是简化版命令（依次在终端执行）：

```bash
# 1. 配置软件源
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" \
            > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update

# 2. 安装 ros-noetic-desktop-full（含 turtlesim、rqt_graph 等工具）
sudo apt install ros-noetic-desktop-full

# 3. 配置环境变量（每次开终端自动 source）
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 4. 安装 rosdep（用于解析包依赖）
sudo apt install python3-rosdep python3-rosinstall \
                 python3-rosinstall-generator python3-wstool build-essential
sudo rosdep init
rosdep update
```

## 三、编译本实验工作空间

解压压缩包之后，进入 `catkin_ws/` 目录第一次执行 `catkin_make`：

```bash
cd catkin_ws
catkin_make
source devel/setup.bash
```

> 之后每次开新终端只需要 `source devel/setup.bash` 即可。

如果脚本没有执行权限，先一次性赋予：

```bash
chmod +x src/plumbing_pub_sub/scripts/*.py
chmod +x src/plumbing_server_client/scripts/*.py
chmod +x src/turtle_control/scripts/*.py
```

## 四、运行实验

### 4.1 小乌龟圆周运动 + 位姿订阅

```bash
roslaunch turtle_control turtle_full.launch
```

启动后弹出 turtlesim 仿真窗口，小乌龟以线速度 1.0、角速度 0.5 作圆周运动；终端持续打印位姿数据（x, y, theta, linear_velocity, angular_velocity）。

### 4.2 话题通信（talker / listener）

```bash
roslaunch plumbing_pub_sub pubsub.launch
```

talker 节点以 10 Hz 向 `/chatter` 发布字符串 `Hello ROS Python N`，listener 节点订阅并打印 `我听见: Hello ROS Python N`。

也可以分两个终端：

```bash
# 终端 A
rosrun plumbing_pub_sub talker.py
# 终端 B
rosrun plumbing_pub_sub listener.py
```

### 4.3 服务通信（AddInts）

自定义服务名：`AddInts_py`，类型：`plumbing_server_client/AddInts`，请求 `int32 num1, num2`，响应 `int32 sum`。

```bash
# 终端 A：服务端
rosrun plumbing_server_client addints_server.py

# 终端 B：客户端，提交两个整数
rosrun plumbing_server_client addints_client.py 10 20
```

或一次性启动：

```bash
roslaunch plumbing_server_client addints.launch
```

预期输出：
- 服务端打印 `服务器收到请求: num1 = 10, num2 = 20`
- 客户端打印 `响应结果: 30`

如果客户端提交负数，服务端会记录错误日志并返回默认响应。

## 五、查看计算图

```bash
rosnode list                          # 列出所有活动节点
rostopic list -v                      # 列出话题及其订阅发布关系
rostopic info /turtle1/cmd_vel        # 查看具体话题拓扑
rosmsg info geometry_msgs/Twist       # 查看消息字段
rqt_graph                             # 节点关系可视化
```

## 六、工程结构

```
catkin_ws/
└── src/
    ├── plumbing_pub_sub/         # 话题通信
    │   ├── scripts/talker.py
    │   ├── scripts/listener.py
    │   └── launch/pubsub.launch
    ├── plumbing_server_client/   # 服务通信
    │   ├── srv/AddInts.srv
    │   ├── scripts/addints_server.py
    │   ├── scripts/addints_client.py
    │   └── launch/addints.launch
    └── turtle_control/           # 小乌龟圆周运动
        ├── scripts/circle_pub.py
        ├── scripts/pose_sub.py
        └── launch/turtle_full.launch
```

## 七、关键参数

| 项 | 值 |
|---|---|
| `/chatter` 发布频率 | 10 Hz，`std_msgs/String` |
| `/turtle1/cmd_vel` 速度 | `linear.x = 1.0`，`angular.z = 0.5` |
| `AddInts` 服务 | `int32 num1, num2 → int32 sum`，负数返回默认响应 |
| 节点名 | `talker_py`、`listener_py`、`circle_pub`、`pose_sub`、`addints_server_py`、`addints_client_py` |

## 八、常见问题

**Q：`rosrun ... talker.py` 提示找不到脚本？**
确认两件事：① 在 catkin_ws 目录下执行过 `source devel/setup.bash`；② Python 脚本具有执行权限（参见第三节末尾的 `chmod +x`）。

**Q：`from plumbing_server_client.srv import AddInts` 提示模块找不到？**
需要先 `catkin_make` 让自定义服务 `.srv` 文件生成对应的 Python 模块；再 `source devel/setup.bash` 使生成模块加入 PYTHONPATH。

**Q：客户端先于服务端启动会怎样？**
本实验客户端使用了 `rospy.wait_for_service("AddInts_py")`，会阻塞等待服务出现，不会立即报错。如果服务端始终没启动，客户端会一直阻塞——可以 `Ctrl+C` 终止。
