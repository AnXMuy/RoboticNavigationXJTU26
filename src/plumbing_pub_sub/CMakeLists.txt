cmake_minimum_required(VERSION 3.0.2)
project(plumbing_pub_sub)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
)

catkin_package()

include_directories(${catkin_INCLUDE_DIRS})

add_executable(demo01_pub_node src/demo01_pub.cpp)
add_executable(demo02_sub_node src/demo02_sub.cpp)

target_link_libraries(demo01_pub_node ${catkin_LIBRARIES})
target_link_libraries(demo02_sub_node ${catkin_LIBRARIES})

install(TARGETS demo01_pub_node demo02_sub_node
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
