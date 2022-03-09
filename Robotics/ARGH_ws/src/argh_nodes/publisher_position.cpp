#include <ros/ros.h>

//inlcuded to publish converted inputs to subscriber positioning script
#include <geometry_msgs/Pose.h>
//#include <geometry_msgs/Point.h>
//#include <geometry_msgs/Quaternion.h>

//stuff for some dumb stuff
#include <tf2/LinearMath/Quaternion.h>

//for user input
#include <stdio.h>
#include <std_msgs/String.h>
#include <stdlib.h>
#include <math.h>

/*
	check_output

	Purpose: Used for input loops to check desired position and orientation are within predefined ranges
		Position Range: [-1000 , 1000] mm
		Angle range: [0, 2*pi] radians

	Inputs: 
		check_value: double value to run check on
		type: boolean value to determine which check to run
*/


bool check_output( double check_val, bool type ){
	
	
	if(type){

		//run position check
		if( ( check_val > 1000 ) || ( check_val < -1000 ) ){
			return true;
		} else{
			return false;
		}

	} else{
		//run angle check
		if( ( check_val > 360 ) || ( check_val < 0 ) ){
			return true;
		} else{
			return false;
		}
	}
	
}

/*
	main script

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
	ros::Publisher pub = nh.advertise<geometry_msgs::Pose>("arm_commanded_pose", 1000);


	//initializing inputs for commanded position
	std::string input_x, input_y, input_z, input_roll, input_pitch, input_yaw;

	//initialize booleans
	bool output_x, output_y, output_z , output_roll, output_pitch, output_yaw; 
	double *publish_array;

	//initialize array
	publish_array = (double*)malloc(6 * sizeof(double)); 

	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	User inputs for x,y,z positions

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/

	//user input for x position
	std::cout << "X position as float [mm]: ";
	std::getline(std::cin, input_x);

	//convert input to double
	publish_array[0] = std::stod(input_x);

	//user input for y position
	std::cout << "Y position as float [mm]: ";
	std::getline(std::cin, input_y);

	//convert input to double
	publish_array[1] = std::stod(input_y);

	//user input for z position
	std::cout << "Z position as float [mm]: ";
	std::getline(std::cin, input_z);

	//convert input to double
	publish_array[2] = std::stod( input_z );

	//check that outputs are within bounds of [-1000, 1000] mm
	output_x = check_output( publish_array[0] , true);
	output_y = check_output( publish_array[1] , true );
	output_z = check_output( publish_array[2] , true);

	//if outputs are not within bounds continue until they are
	while( output_x || output_y || output_z ){
		
		//display to user outputs
		std::cout << "please enter a value for positions within bounds of [-1000, 1000] mm \n";
		
		if(output_x){
			//check x
			
			std::cout << "X position as float [mm]: ";
			std::getline(std::cin, input_x);
			publish_array[0] = std::stod(input_x);
			output_x = check_output(publish_array[0],true);

		}else if(output_y){
			//check y
			
			std::cout << "Y position as float [mm]: ";
			std::getline(std::cin, input_y);
			publish_array[1] = std::stod(input_y);
			output_y = check_output(publish_array[1],true);

		}else if(output_z){
			//check z

			std::cout << "Z position as float [mm]: ";
			std::getline(std::cin, input_z);
			publish_array[2] = std::stod(input_z);
			output_z = check_output(publish_array[2],true);

		}
	}

		/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	User inputs for roll, pitch and yaw

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/

	//user input for roll
	std::cout << "Roll as float [deg]: ";
	std::getline(std::cin, input_roll);

	//convert input to double
	publish_array[3] = std::stod(input_roll);

	//user input for pitch
	std::cout << "Pitch as float [deg]: ";
	std::getline(std::cin, input_pitch);

	//convert input to double
	publish_array[4] = std::stod(input_pitch);

	//user input for yaw
	std::cout << "Yaw as float [deg]: ";
	std::getline(std::cin, input_yaw);

	//convert input to double
	publish_array[5] = std::stod(input_yaw);

	//check that outputs are within bounds of [-1000, 1000] mm
	output_roll = check_output(publish_array[3], false);
	output_pitch = check_output(publish_array[4] , false);
	output_yaw = check_output(publish_array[5] , false);

	//if outputs are not within bounds continue until they are
	while( output_roll || output_pitch || output_yaw ){
		
		//display to user outputs
		std::cout << "please enter a value for positions within bounds of [0, 360] deg \n";
		
		if(output_roll){
			//check roll
			
			std::cout << "Roll as float [deg]: ";
			std::getline(std::cin, input_x);
			publish_array[3] = std::stod(input_roll);
			output_roll = check_output(publish_array[3], false);

		}else if(output_pitch){
			//check pitch
			
			std::cout << "Pitch as float [deg]: ";
			std::getline(std::cin, input_pitch);
			publish_array[4] = std::stod(input_y);
			output_pitch = check_output(publish_array[4], false);

		}else if(output_yaw){
			//check yaw

			std::cout << "Yaw as float [deg]: ";
			std::getline(std::cin, input_z);
			publish_array[5] = std::stod(input_yaw);
			output_yaw = check_output(publish_array[5],false);

		}
	}


	
   /*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	prepping for publishing 

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/


	//convert inputs to meters
	for(int i = 0; i <= 2; i++ ){
		publish_array[i] = publish_array[i]/1000;
	} 

	//convert inputs to radians
	for(int i = 3; i <= 5; i++ ){
		publish_array[i] = publish_array[i] * (M_PI/180);
	} 

	// convert Roll, Pitch and Yaw to quantfuck
	tf2::Quaternion myQuaternion;
   	myQuaternion.setRPY( publish_array[3], publish_array[4], publish_array[5] );  
   	myQuaternion.normalize();
   	
	/*
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	messages publishing 

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/
	
	//creating first object to publish
	geometry_msgs::Pose msg1;

	//filling messege
	msg1.position.x = publish_array[0]; 
	msg1.position.y = publish_array[1];
	msg1.position.z = publish_array[2];
	msg1.orientation.x = myQuaternion[0];
	msg1.orientation.y = myQuaternion[1];
	msg1.orientation.z = myQuaternion[2];
	msg1.orientation.w = myQuaternion[3];
	
	//publishing message
	pub.publish(msg1);

	//output to console
	ROS_INFO_STREAM( "Message details sent: "
		<< " X position=> " << msg1.position.x 
		<< " Y position=> " << msg1.position.y
		<< " Z position=> " << msg1.position.z 
		<< "X orientation=> " << msg1.orientation.x
		<< "Y orientation=> " << msg1.orientation.y
		<< "Z orientation=> " << msg1.orientation.z
		<< "W orientation=> " << msg1.orientation.w
		);




	free(publish_array);
}