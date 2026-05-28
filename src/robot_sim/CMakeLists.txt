cmake_minimum_required(VERSION 3.0.2)
project(robot_sim)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  robot_state_publisher
  xacro
)

catkin_package()

install(DIRECTORY launch urdf worlds
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
