/*
_______  _____  _    _ _______      __   _  _____  ______  _______
|  |  | |     |  \  /  |______      | \  | |     | |     \ |______
|  |  | |_____|   \/   |______      |  \_| |_____| |_____/ |______

*/                                                                  

/*
References
	http://docs.ros.org/en/kinetic/api/moveit_tutorials/html/doc/move_group_interface/move_group_interface_tutorial.html
	https://roboticscasual.com/ros-tutorial-pick-and-place-task-with-the-moveit-c-interface/
*/

#include <ros/ros.h>

//for subscring to boolean passed from sensing node
#include <std_msgs/Bool.h>

//for publishing move count to control node
#include <std_msgs/Int32.h>

//for pose and oreintation of tcp
#include <geometry_msgs/Pose.h>

//for moving sensor following pick and place example and moveit c++ interface tutorials
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>
#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>
#include <moveit_visual_tools/moveit_visual_tools.h>

//for standard dumb stuff
#include <stdio.h>
#include <std_msgs/String.h>
#include <stdlib.h>
#include <vector>

//for c++ sleep
#include <chrono>
#include <thread>

//using a global variable for initiailizing sensing position and initializing planning group
int current_sensor_position { 1 };
static const std::string PLANNING_GROUP_ARM = "manipulator";

//storing joint positions for positions home -> 1 -> 2 -> 3 
//elements go by shoulder_pan, shoulder_lift, elbow_joint, wrist_1, wrist_2, wrist_3
const std::vector<double> home_pos{5.96377277374, -0.5757077497, -2.556312084197, -3.14978327373, -0.3186467329608,  3.139601707458496};
const std::vector<double> first_pos{4.1757049560546875, -1.9448801479735316, -2.182875156402588, -3.8517877064146937, -1.5011804739581507, 2.652855634689331};
const std::vector<double> second_pos{5.128342628479, -1.71154989818715, -2.543005466461, -3.7090360126891078, -1.6590359846698206, 3.584813117980957};
const std::vector<double> third_pos{5.951443672180176, -1.8237282238402308, -2.34622882041931152, -3.725156923333639, -1.7076171080218714, 4.421555519104004};

//storing tcp positions relative to base for positions 1 -> 3
const std::vector<double> first_pos_tcp{0.36415, 0.25561 , 0.174};
const std::vector<double> second_pos_tcp{0.0663, 0.25562 , 0.174};
const std::vector<double> third_pos_tcp{-0.2547, 0.25562 , 0.174};

 /*
	Name: MoveSensor
	Purpose: Publish Twice and Subscriber node which is in charge of moving the sensor to its three positions.
			 Will begin after reciving a boolean true value published on the sensing_node_boolean_move topic 
			 and after completing move will reset by publsihing a boolean false on the same topic it subscribes to. 
	Inputs:
		"sensing_node_boolean_move", std_msgs/Bool : boolean value that will control when a move needs to happen
	Outputs:
		"sensing_node_input" , std_msgs/Bool: used to start the sensing node again
		terminal: notifying user that robotic arm is moving sensor 
	
	Updates to be made:
																																																																						

	Author: Connor O'Reilly
	Company: ARGH Robotics
	Last Edited: 04/08/2022
	Email: coor1752@colorado.edu
*/


//create class for publishing and subscribing for sensor positioning 
class MoveSensor
{
public:
  MoveSensor()
  {
    //publsihing sensor position to move_counter topic
    pub_1 = n_.advertise<std_msgs::Int32>("move_counter", 1000);

    //publishing sensor boolean value to sensing_node_boolean_move
    pub_2 = n_.advertise<std_msgs::Bool>("sensing_node_boolean_move", 1000);
    
    //publishing command to gripper control
    pub_3 = n_.advertise<std_msgs::String>("control_gripper", 1000);
    
    pub_4 = n_.advertise<std_msgs::Bool>("sensing_node_input", 1000);

    //subscribing to the boolean passed from the sensing node to tell whether we move or not 
    sub_1 = n_.subscribe("sensing_node_boolean_move", 1000, &MoveSensor::MoveSensor_callback, this);
  
  }

  // call back runs on sensing_node_boolean_move, will move the sensor to the next position (1->2->3), 
  // once a move is requested when the sensor is a position three, the position counter will be reset back to one 

  void MoveSensor_callback(const std_msgs::Bool& input)
  {

  	//intialize rate
  	ros::Rate rate(2);

  	//initializing messages to be published
    std_msgs::Int32 sensor_position; //integer for sensor position
    std_msgs::Bool move_the_sensor_bool; //boolean to stop computations in this node
    std_msgs::String control_gripper; //string to tell the gripper what to do
    std_msgs::Bool tell_sense_to_go;
    if(input.data == true){
    	
    	//insantiate plan group
  		moveit::planning_interface::MoveGroupInterface move_group_interface_arm(PLANNING_GROUP_ARM);
  		moveit::planning_interface::MoveGroupInterface::Plan move_plan;
			

			//initialize variables to be used inside of switch statement, used for cartesian move	
  		geometry_msgs::Pose target_pose1;

  		//for cartesian planning
  		geometry_msgs::Pose cartesian_target_pose1;
			std::vector<geometry_msgs::Pose> waypoints;
			moveit_msgs::RobotTrajectory trajectory;
			double fraction;
			moveit::planning_interface::MoveGroupInterface::Plan  goal_plan;
			moveit_msgs::Constraints test_constraints;
			moveit_msgs::OrientationConstraint ocm;

			//initialize path constraints
			ocm.link_name = "r_wrist_roll_link";
	    ocm.header.frame_id = "base_link";
	    ocm.orientation.w = 1.0;
	    ocm.absolute_x_axis_tolerance = 0.001;
	    ocm.absolute_y_axis_tolerance = 0.0;
	    ocm.absolute_z_axis_tolerance = 0.0;
	    ocm.weight = 1.0;
	    test_constraints.orientation_constraints.push_back(ocm);

  		//move to the home position just incase we didnt return to home before
  		move_group_interface_arm.setJointValueTarget(home_pos);
  		move_group_interface_arm.move();

  		//open gripper before moving to first position
  		control_gripper.data = "open_fast_hard";
  		pub_3.publish(control_gripper);
    	rate.sleep();

    	//check current sensor position 
    	switch(current_sensor_position){
    		case 1: 
    			//if current position is equal to one move sensor to position two
    			ROS_INFO_STREAM("Moving Sensor from position 1 -> 2..."); //inform  user we are moving the sensor
    			
    			//move to position 1 from home
    			move_group_interface_arm.setJointValueTarget(first_pos);
    			move_group_interface_arm.move();

			    move_group_interface_arm.setPathConstraints(test_constraints);

    			//position 1 has been reached
    			//close the gripper and grasp sensor mount
    			control_gripper.data = "close_fast_hard";
    			pub_3.publish(control_gripper);
    			rate.sleep();
    			//move to position 2
    			 
    			//move to position two

    			//alright so set the first waypoint
    			cartesian_target_pose1 = move_group_interface_arm.getCurrentPose().pose;
    			//push back to waypoints
    			waypoints.push_back(cartesian_target_pose1);
    			//current pose set get next
    			cartesian_target_pose1.position.x = second_pos_tcp.at(0);
    			//set it 
    			waypoints.push_back(cartesian_target_pose1);
    			fraction = move_group_interface_arm.computeCartesianPath(waypoints, 0.01, 0.0, trajectory);
    			std::this_thread::sleep_for(std::chrono::seconds(5));

    			goal_plan.trajectory_ = trajectory;
    			move_group_interface_arm.execute(goal_plan);
    			rate.sleep();
    			//open gripper
    			control_gripper.data = "open_fast_hard";
    			pub_3.publish(control_gripper);
    			rate.sleep();

    			//clear path constraints
    			move_group_interface_arm.clearPathConstraints();
    			

    			//after gripper is open reaturn to the home position
    			move_group_interface_arm.setJointValueTarget(home_pos);
    			move_group_interface_arm.move();

    			//inform to user 
    			ROS_INFO_STREAM("Sensor moved from position: ONE to position: TWO");
    			current_sensor_position = 2; //update sensor position 
    			break;

			case 2:
				//if current position is equal to one move sensor to position two

    			ROS_INFO_STREAM("Moving Sensor from position 2 -> 3..."); //inform  user we are moving the sensor
    			//move to position 1 from home
    			move_group_interface_arm.setJointValueTarget(second_pos);
    			move_group_interface_arm.move();

    			//position 2 has been reached
    			//close the gripper and grasp sensor mount
    			control_gripper.data = "close_fast_hard";
    			pub_3.publish(control_gripper);
    			rate.sleep();
    			//move to position 2
    			 
    			//move to position two

    			//alright so set the first waypoint
    			cartesian_target_pose1 = move_group_interface_arm.getCurrentPose().pose;
    			//push back to waypoints
    			waypoints.push_back(cartesian_target_pose1);
    			//current pose set get next
    			cartesian_target_pose1.position.x = third_pos_tcp.at(0);
    			//set it 
    			waypoints.push_back(cartesian_target_pose1);
    			fraction = move_group_interface_arm.computeCartesianPath(waypoints, 0.01, 0.0, trajectory);
    			std::this_thread::sleep_for(std::chrono::seconds(4));
    			goal_plan.trajectory_ = trajectory;
    			move_group_interface_arm.execute(goal_plan);
    			rate.sleep();
    			//open gripper
    			control_gripper.data = "open_fast_hard";
    			pub_3.publish(control_gripper);
    			rate.sleep();

    			//clear path constraints
    			move_group_interface_arm.clearPathConstraints();

    			//after gripper is open reaturn to the home position
    			move_group_interface_arm.setJointValueTarget(home_pos);
    			move_group_interface_arm.move();
    			rate.sleep();
    			//inform to user 
    			ROS_INFO_STREAM("Sensor moved from position: TWO to position: THREE");
    			current_sensor_position = 3; //update sensor position 
    			break;

			case 3:
				//if current position is equal to one move sensor to position two

    			ROS_INFO_STREAM("Moving Sensor from position 3 -> 1... ALL SENSING POSITIONS CHECKED"); //inform  user we are moving the sensor
    			


    			//move to position 1 from home
    			move_group_interface_arm.setJointValueTarget(third_pos);
    			move_group_interface_arm.move();

			    move_group_interface_arm.setPathConstraints(test_constraints);

    			//position 1 has been reached
    			//close the gripper and grasp sensor mount
    			control_gripper.data = "close_fast_hard";
    			rate.sleep();
    			pub_3.publish(control_gripper);
    			rate.sleep();
    			//move to position 2
    			 
    			//move to position two

    			//alright so set the first waypoint
    			cartesian_target_pose1 = move_group_interface_arm.getCurrentPose().pose;
    			//push back to waypoints
    			waypoints.push_back(cartesian_target_pose1);
    			//current pose set get next
    			cartesian_target_pose1.position.x = first_pos_tcp.at(0);
    			//set it 
    			waypoints.push_back(cartesian_target_pose1);
    			fraction = move_group_interface_arm.computeCartesianPath(waypoints, 0.01, 0.0, trajectory);
    			std::this_thread::sleep_for(std::chrono::seconds(5));
    			goal_plan.trajectory_ = trajectory;
    			move_group_interface_arm.execute(goal_plan);
    			rate.sleep();
    			//open gripper
    			control_gripper.data = "open_fast_hard";
    			pub_3.publish(control_gripper);
    			rate.sleep();

    			//clear path constraints
    			move_group_interface_arm.clearPathConstraints();
    			//after gripper is open reaturn to the home position
    			move_group_interface_arm.setJointValueTarget(home_pos);
    			move_group_interface_arm.move();

    			//inform to user 
    			ROS_INFO_STREAM("Sensor moved from position: THREE to position: ONE");
    			current_sensor_position = 1; //update sensor position 
    			break;
			default:
				ROS_FATAL_STREAM("This switch case in MoveSensor_callback should not be reached");
				ros::shutdown();
				break;
    	}


    	//publish current sensor location so other nodes are in the loop, lmaoooo
    	sensor_position.data = current_sensor_position;
    	pub_1.publish(sensor_position);
    	rate.sleep();
    	//reset message so node does not continue to move sensor or update sensor position
    	move_the_sensor_bool.data = false;
    	pub_2.publish(move_the_sensor_bool);
    	rate.sleep();

    	control_gripper.data = "start";
    	pub_3.publish(control_gripper);
    	rate.sleep();
    	

    	tell_sense_to_go.data = true;
    	pub_4.publish(tell_sense_to_go);
    	rate.sleep();

    }

  }

private:
  ros::NodeHandle n_; 
  ros::Publisher pub_1;
  ros::Publisher pub_2;
  ros::Publisher pub_3;
  ros::Publisher pub_4;
  ros::Subscriber sub_1;

};//End of class MoveSensor



int main(int argc, char **argv){

	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	initialization

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/

	//initializing ros and node for publishing 
	ros::init(argc, argv, "move_node");
	ros::NodeHandle nh;
	
	ros::AsyncSpinner spinner(0);
	spinner.start();
	
	//creating object of class SubscribeAndPublish that will take care of everything
	MoveSensor MoveSensorObject;
	
	ros::waitForShutdown();
	
}