cmake_minimum_required(VERSION 3.5)
project(plumbing_server_client)

find_package(catkin REQUIRED COMPONENTS rospy std_msgs message_generation)

add_service_files(FILES AddInts.srv)
generate_messages(DEPENDENCIES std_msgs)

catkin_package(CATKIN_DEPENDS message_runtime)

catkin_install_python(PROGRAMS
  scripts/addints_server.py
  scripts/addints_client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
