# Copyright(c) 2020 eaibot limited.
cmake_minimum_required(VERSION 2.8)

project(ydlidar_ros_driver)

option(YDLIDAR_USE_VENDORED_SDK "Build with the bundled YDLidar-SDK sources." ON)

if(YDLIDAR_USE_VENDORED_SDK)
  set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
  set(BUILD_CSHARP OFF CACHE BOOL "" FORCE)
  set(BUILD_TEST OFF CACHE BOOL "" FORCE)
  add_subdirectory(YDLidar-SDK EXCLUDE_FROM_ALL)

  set(YDLIDAR_SDK_INCLUDE_DIRS
    ${CMAKE_CURRENT_SOURCE_DIR}/YDLidar-SDK
    ${CMAKE_CURRENT_SOURCE_DIR}/YDLidar-SDK/src
    ${CMAKE_CURRENT_BINARY_DIR}/YDLidar-SDK
  )
  set(YDLIDAR_SDK_LIBRARIES ydlidar_sdk)
else()
  find_package(ydlidar_sdk REQUIRED)
endif()

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  sensor_msgs
  std_srvs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy sensor_msgs std_srvs
)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose Release or Debug" FORCE)
endif()

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${YDLIDAR_SDK_INCLUDE_DIRS}
)

add_executable(${PROJECT_NAME}_node src/ydlidar_ros_driver.cpp)
target_link_libraries(${PROJECT_NAME}_node
  ${catkin_LIBRARIES}
  ${YDLIDAR_SDK_LIBRARIES}
)

install(TARGETS ${PROJECT_NAME}_node
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch startup
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
