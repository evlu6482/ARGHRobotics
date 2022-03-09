#include <ros/ros.h>

//to subscribe to ros message
#include  <geometry_msgs/Pose.h>

//for other shit
#include <stdio.h>
#include <std_msgs/String.h>
#include <stdlib.h>
#include <math.h>

// for outputs std:::setpercision
#include <iomanip>

/*
	iHaveTheShitsCurrently Callback Function 
	
	Purpose: Just getting used to publisher subscriber relationships, 
	hopefully it goes better than my current relationship

	Inputs: 



*/
void iHaveTheShitsCurrently(const geometry_msgs::Pose& msg1){

	ROS_INFO_STREAM( "Message details recieved: "
		<< " X position=> " << msg1.position.x 
		<< " Y position=> " << msg1.position.y
		<< " Z position=> " << msg1.position.z 
		<< " X orientation=> " << msg1.orientation.x
		<< " Y orientation=> " << msg1.orientation.y
		<< " Z orientation=> " << msg1.orientation.z
		<< " W orientation=> " << msg1.orientation.w
		);
}

/*
	main script

	Purpose: to check we are recieving published messages of type geometry_msgs/Pose.h on the topic of 
	arm_commanded_pose for user inputs for commanded X,Y and Z for the goal state of the end-effector positioning 
	and Roll, Pitch and Yaw for the goal state of the end-effector
	
	Inputs: 
		none atm
	Outputs:
		just recieved messages to terminal of X,Y,Z position and 



*/
int main(int argc, char **argv){

	//initializing ros system and node
	ros::init(argc, argv, "argh_point_subscriber_node");
	ros::NodeHandle nh;


	//creating subscriber object
	ros::Subscriber sub = nh.subscribe("arm_commanded_pose", 1000, &iHaveTheShitsCurrently);

	//leting ros take over
	ros::spin();




}