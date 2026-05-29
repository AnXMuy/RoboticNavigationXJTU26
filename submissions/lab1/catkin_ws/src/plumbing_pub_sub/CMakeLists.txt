cmake_minimum_required(VERSION 3.5)
project(plumbing_pub_sub)

find_package(catkin REQUIRED COMPONENTS rospy std_msgs)
catkin_package()

catkin_install_python(PROGRAMS
  scripts/talker.py
  scripts/listener.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
