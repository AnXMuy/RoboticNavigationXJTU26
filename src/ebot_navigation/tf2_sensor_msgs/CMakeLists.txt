cmake_minimum_required(VERSION 3.0.2)
project(tf2_sensor_msgs)

find_package(catkin REQUIRED COMPONENTS geometry_msgs sensor_msgs tf2 tf2_ros)

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS geometry_msgs sensor_msgs tf2 tf2_ros
)

include_directories(include ${catkin_INCLUDE_DIRS})

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
)
