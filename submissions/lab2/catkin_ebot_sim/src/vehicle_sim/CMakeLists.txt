cmake_minimum_required(VERSION 3.0.2)
project(vehicle_sim)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  rospy
  std_msgs
  tf2
  tf2_geometry_msgs
  tf2_ros
  urdf
  xacro
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/vehicle_sim.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch urdf rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
