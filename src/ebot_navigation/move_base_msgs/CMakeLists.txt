cmake_minimum_required(VERSION 3.0.2)
project(move_base_msgs)

find_package(catkin REQUIRED COMPONENTS
  actionlib_msgs
  geometry_msgs
  message_generation
  std_msgs
)

add_action_files(
  DIRECTORY action
  FILES MoveBase.action
)

add_message_files(
  DIRECTORY msg
  FILES RecoveryStatus.msg
)

generate_messages(
  DEPENDENCIES actionlib_msgs geometry_msgs std_msgs
)

catkin_package(
  CATKIN_DEPENDS actionlib_msgs geometry_msgs message_runtime std_msgs
)
