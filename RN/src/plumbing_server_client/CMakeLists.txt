cmake_minimum_required(VERSION 3.0.2)
project(plumbing_server_client)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  roscpp
  rospy
  std_msgs
)

add_service_files(
  FILES
  AddInts.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime roscpp rospy std_msgs
)

include_directories(${catkin_INCLUDE_DIRS})

add_executable(demo01_server_node src/demo01_server.cpp)
add_executable(demo02_client_node src/demo02_client.cpp)

add_dependencies(demo01_server_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})
add_dependencies(demo02_client_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

target_link_libraries(demo01_server_node ${catkin_LIBRARIES})
target_link_libraries(demo02_client_node ${catkin_LIBRARIES})

install(TARGETS demo01_server_node demo02_client_node
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
