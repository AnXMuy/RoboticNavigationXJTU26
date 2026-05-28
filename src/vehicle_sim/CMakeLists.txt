cmake_minimum_required(VERSION 3.0.2)
project(vehicle_sim)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  rospy
  tf2_ros
  xacro
)

catkin_package()

catkin_install_python(PROGRAMS
  scripts/vehicle_sim.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch urdf meshes rviz
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
