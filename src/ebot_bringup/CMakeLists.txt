cmake_minimum_required(VERSION 3.0.2)
project(ebot_bringup)

find_package(catkin REQUIRED)

catkin_package()

install(DIRECTORY launch config maps
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
