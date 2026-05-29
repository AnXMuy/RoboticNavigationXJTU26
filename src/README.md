# Group12 Robotic Navigation Source Workspace

This `src` directory is the catkin source workspace for experiments 1-5.
Teacher demo packages are copied into the matching package groups without
changing their launch/config defaults.

## Experiment 1

```bash
roslaunch plumbing_pub_sub pub_sub.launch
roslaunch plumbing_server_client server.launch
roslaunch plumbing_server_client client.launch num1:=10 num2:=20
```

## Experiment 2

```bash
roslaunch vehicle_sim vehicle_sim_rviz.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

## Experiment 3

Simulation:

```bash
roslaunch ebot_bringup bringup.launch simulation:=true
roslaunch ebot_bringup slam_gmapping.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

Real robot:

```bash
roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup slam_hector.launch
rosrun teleop_twist_keyboard teleop_twist_keyboard.py
cd src/ebot_bringup/maps
rosrun map_server map_saver -f nav
```

## Experiment 4

```bash
roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup test_amcl.launch
rviz
```

## Experiment 5

```bash
roslaunch ebot_bringup bringup.launch
roslaunch ebot_bringup test_nav.launch
rviz
```

Replace `ebot_bringup/maps/nav.yaml` and `nav.pgm` with the real map generated
in experiment 3 before running localization or navigation on the robot.
