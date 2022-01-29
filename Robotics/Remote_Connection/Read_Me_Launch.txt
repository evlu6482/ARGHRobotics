Files to make life easier if anyone wants to mess with the robot on pc
easiest to just create catkin ws and move launch folder to src folder
need to change ip on polyscope program to match your machines, its like ip addr show in linux i think
also download ur driver stuff 


roslaunch ur_calibration calibration_correction.launch \ robot_ip:=192.168.0.12 \ target_filename:="$(rospack find argh_ur_launch)/etc/ur10e_calibration.yaml"


roslaunch ur_robot_driver ur10e_bringup.launch robot_ip:=192.168.0.12 \
  kinematics_config:=$(rospack find argh_ur_calibration)/etc/ur10e_calibration.yaml


Because i am an idiot this is how to load teleop
need to download vcxrsv and make sure to set display to 0

  one terminal: 
  source devel/.bash
  roscore

  second terminal:
  allows robot to take command inputs
  roslaunch ur_robot_driver ur10e_bringup.launch robot_ip:=192.168.0.12

  third terminal currently
  export DISPLAY:=0 

  allows x window to show joint trajectory 
  then joint controller

  rosrun rqt_joint_trajectory_controller rqt_joint_trajectory_controller