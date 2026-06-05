cmake_minimum_required(VERSION 3.5)
project(turtle_control)

find_package(catkin REQUIRED COMPONENTS rospy)
catkin_package()

catkin_install_python(PROGRAMS
  scripts/circle_pub.py
  scripts/pose_sub.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
