#include <ros/ros.h>

//inlcuded to publish converted inputs to subscriber positioning script
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Quaternion.h>

//for user input
#include <stdio.h>
#include <std_msgs/String.h>
#include <stdlib.h>


/*
	Purpose: will take user inputs for commanded X,Y and Z for goal state of end-effector positioning and Roll, Pitch and Yaw for the goal state of end-effector 
	
	Inputs:
		input_x = string of float goal state x positioning of end effector in millimeters, later to be converted to float
		input_y = string of float goal state y positioning of end effector in millimeters, later to be converted to float
		input_z = string of float goal state z positioning of end effector in millimeters, later to be converted to float

	Publishing:
		geometry_msgs/Pose

	Author: Connor O'Reilly
	Last Edited: 03/07/2022
	email:coor1752@colorado.edu		

*/

bool check_output( double position ){
	if( ( position > 1000 ) || ( position < -1000 ) ){
		return true;
	} else{
		return false;
	}
}



int main(int argc, char **argv){

	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	initialization

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/

	//initializing node
	ros::init(argc, argv, "argh_point_publisher_node");
	ros::NodeHandle nh;

	//creating publisher object
	ros::Publisher pub = nh.advertise<geometry_msgs::Point>("arm_commanded_pose", 1000);


	//initializing inputs for commanded position
	std::string input_x, input_y, input_z, input_roll, input_pitch, input_yaw;

	//initialize booleans
	bool output_x, output_y, output_z; 
	double *publish_array;

	//initialize array
	publish_array = (double*)malloc(3 * sizeof(double)); 

	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	User inputs

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/

	//user input for x position
	std::cout << "X position as float [mm]: ";
	std::getline(std::cin, input_x);

	//convert input to float
	publish_array[0] = std::stod(input_x);

	//user input for y position
	std::cout << "Y position as float [mm]: ";
	std::getline(std::cin, input_y);

	//convert input to float
	publish_array[1] = std::stod(input_y);

	//user input for z position
	std::cout << "Z position as float [mm]: ";
	std::getline(std::cin, input_z);

	//convert input to float
	publish_array[2] = std::stod(input_z);

	//check that outputs are within bounds of [-1000, 1000] mm
	output_x = check_output(publish_array[0]);
	output_y = check_output(publish_array[1]);
	output_z = check_output(publish_array[2]);

	//if outputs are not within bounds continue until they are
	while( output_x || output_y || output_z ){
		
		//display to user outputs
		std::cout << "please enter a value for positions within bounds of [-1000, 1000] mm \n";
		
		if(output_x){
			//check x
			
			std::cout << "X position as float [mm]: ";
			std::getline(std::cin, input_x);
			publish_array[0] = std::stod(input_x);
			output_x = check_output(publish_array[0]);

		}else if(output_y){
			//check y
			
			std::cout << "Y position as float [mm]: ";
			std::getline(std::cin, input_y);
			publish_array[1] = std::stod(input_y);
			output_y = check_output(publish_array[1]);

		}else if(output_z){
			//check z

			std::cout << "Z position as float [mm]: ";
			std::getline(std::cin, input_z);
			publish_array[2] = std::stod(input_z);
			output_z = check_output(publish_array[2]);

		}
	}


	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	prepping for publishing 

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/


	//convert inputs to meters
	for(int i = 0; i <= 5; i++ ){
		publish_array[i] = publish_array[i]/1000;
	} 

	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	messages publishing 

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/
	
	//creating object to publish
	geometry_msgs::Point msg;

	//filling messege
	msg.x = publish_array[0]; 
	msg.y = publish_array[1];
	msg.z = publish_array[2];


	//publishing message
	pub.publish(msg);

	//output to console
	ROS_INFO_STREAM( "Message details sent: "
		<< " X position=> " << msg.x 
		<< " Y position=> " << msg.y
		<< " Z position=> " << msg.z );

	free(publish_array);
}