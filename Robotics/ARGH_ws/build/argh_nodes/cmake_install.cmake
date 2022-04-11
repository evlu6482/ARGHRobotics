# Install script for directory: /home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/src/argh_nodes

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/argh_nodes/catkin_generated/installspace/argh_nodes.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/argh_nodes/cmake" TYPE FILE FILES
    "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/argh_nodes/catkin_generated/installspace/argh_nodesConfig.cmake"
    "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/argh_nodes/catkin_generated/installspace/argh_nodesConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/argh_nodes" TYPE FILE FILES "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/src/argh_nodes/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/argh_nodes" TYPE PROGRAM FILES "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/argh_nodes/catkin_generated/installspace/gripper_cntrl_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/argh_nodes" TYPE PROGRAM FILES "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/argh_nodes/catkin_generated/installspace/harvest_node.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/argh_nodes" TYPE PROGRAM FILES "/home/argh/Documents/ARGH/ARGHRobotics/Robotics/ARGH_ws/build/argh_nodes/catkin_generated/installspace/sense_node.py")
endif()

