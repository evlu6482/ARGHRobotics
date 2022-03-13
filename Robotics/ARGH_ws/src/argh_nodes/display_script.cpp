#include <ros/ros.h>



//for telling nodes when to start
#include <std_msgs/Bool.h>

//for standard user input
#include <stdio.h>
#include <std_msgs/String.h>
#include <math.h>
#include <stdlib.h>

/*
	Check User Input

	Purpose: just a function to clean things up and check the users input
	
	Input:
		user_input: string that the user inputed
	Output:	
		user_choice: correct user input
*/

int check_user_input(std::string user_input){
	//initialize values
	bool is_good = true;
	//convert string to integer
        int user_choice = std::stoi(user_input); 
	while(is_good){
	 //convert string to integer             
         user_choice = std::stoi(user_input);
		//determine if its a good choice
		switch(user_choice){
			//relating to node selection, if adding more options please add to the switch statement
			
			case 0:
				is_good = false;
				break;
			case 1:
				is_good = false;
				break;
			case 2:
				is_good = false;
				break;
			default:
				std::cout << "Incorrect input detected.\n";
				std::cout << "Please enter either 0 , 1 or 2 or Cntrl C to exit.\n";
				std::cout <<"Input: ";
				std::getline(std::cin, user_input);
		}

	}
	return user_choice;
}


/*
	Main func

	Purpose: will get user input to run certain nodes, as well as display outputs. kinda like the argh control pannel
	inputs: 
		user_choice: converted user intput from string to int, run through check_user_input to handle incorrect inputs
	outputs:
		just log messages to notify user whats happening
	
	help for modifying code:
		adding run options:
			- must modify switch statement in check_user_input to include the relating integer value of run option
			- also must modify node selection comment around line 139 to update the prompt to the user
	
	Author: Connor O'Reilly
	Last Modified: 03/11/2022
        email: coor1752@colorado.edu		
 
*/

int main(int argc, char **argv){
	/*
	 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	                Initialization
	 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	*/
	

	//initializing ros and node	
	ros::init(argc, argv, "argh_control_node");
	ros::NodeHandle nh;

	
		
	
	
	
	//initializing user input and handling cases 
	std::string user_input, publish_topic;
	int user_choice;

	
	/*
          %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                         Display and User Input
          %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
         */
	
	std::cout<<"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
	std::cout<<"-----------------------------------------------------------------------------------------------";
	std::cout<<"░█████╗░██████╗░░██████╗░██╗░░██╗  ██████╗░░█████╗░██████╗░░█████╗░████████╗██╗░█████╗░░██████╗";
	std::cout<<"██╔══██╗██╔══██╗██╔════╝░██║░░██║  ██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗██╔════╝";
	std::cout<<"███████║██████╔╝██║░░██╗░███████║  ██████╔╝██║░░██║██████╦╝██║░░██║░░░██║░░░██║██║░░╚═╝╚█████╗░";
	std::cout<<"██╔══██║██╔══██╗██║░░╚██╗██╔══██║  ██╔══██╗██║░░██║██╔══██╗██║░░██║░░░██║░░░██║██║░░██╗░╚═══██╗";
	std::cout<<"██║░░██║██║░░██║╚██████╔╝██║░░██║  ██║░░██║╚█████╔╝██████╦╝╚█████╔╝░░░██║░░░██║╚█████╔╝██████╔╝";
	std::cout<<"╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝  ╚═╝░░╚═╝░╚════╝░╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░";
	std::cout<<"-----------------------------------------------------------------------------------------------";
	std::cout<<"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
	std::cout<<"\n";
	std::cout<<"\n";
	std::cout<<"\n";
	std::cout<<"please press enter to continue...";
	//record enter pressed
	std::cin.ignore();
	//clear screen and show new display
	system("clear");
	std::cout<<"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
        std::cout<<"-----------------------------------------------------------------------------------------------";
        std::cout<<"░█████╗░██████╗░░██████╗░██╗░░██╗  ██████╗░░█████╗░██████╗░░█████╗░████████╗██╗░█████╗░░██████╗";
        std::cout<<"██╔══██╗██╔══██╗██╔════╝░██║░░██║  ██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗██╔════╝";
        std::cout<<"███████║██████╔╝██║░░██╗░███████║  ██████╔╝██║░░██║██████╦╝██║░░██║░░░██║░░░██║██║░░╚═╝╚█████╗░";
        std::cout<<"██╔══██║██╔══██╗██║░░╚██╗██╔══██║  ██╔══██╗██║░░██║██╔══██╗██║░░██║░░░██║░░░██║██║░░██╗░╚═══██╗";
        std::cout<<"██║░░██║██║░░██║╚██████╔╝██║░░██║  ██║░░██║╚█████╔╝██████╦╝╚█████╔╝░░░██║░░░██║╚█████╔╝██████╔╝";
        std::cout<<"╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝  ╚═╝░░╚═╝░╚════╝░╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░";
        std::cout<<"-----------------------------------------------------------------------------------------------";
        std::cout<<"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++";
        std::cout<<"\n";
        std::cout<<"\n";
        std::cout<<"\n";
        std::cout<<"------------------\n";
	std::cout<<"Select Run Option:\n";
	std::cout<<"------------------\n";
	//node selection
	std::cout<<"0: Shut down\n";
	std::cout<<"1: Detect tomatos\n";
	std::cout<<"2: Harvest tomatos\n";
	std::cout<<"------------------\n";
	//get user input for run option
	std::cout<<"Input:  ";
	std::getline(std::cin, user_input);
	
	//check user input
	user_choice = check_user_input(user_input);
	

	

	//will run until user enters cntrl c of ros node terminates due to error
	//probably just have subscriber nodes pin once
	
	while(ros::ok()){
		//display to user selected option
		//create publisher object relating to user input
		switch(user_choice){
			case 0:
				ros::shutdown();
				break;
			case 1: 
				//set topic to publish to 
				publish_topic = "detect_tomatos";
				
				break;
			case 2:
				//create publisher object relating to case
				publish_topic = "harvest_tomatos";
				break;

		}
		ros::Publisher pub = nh.advertise<std_msgs::Bool>(publish_topic,1000);
		std_msgs::Bool msg;
		msg.data = true;
		pub.publish(msg);
		ROS_INFO_STREAM("message sent: "
				<< "boolean " << msg.data
			       );
		//redo user display
		std::cout<<"Select Run Option:\n";     
	        std::cout<<"------------------\n";
	        //node selection            
	        std::cout<<"0: Shut down\n";
	        std::cout<<"1: Detect tomatos\n";      
	    	std::cout<<"2: Harvest tomatos\n";     
	        std::cout<<"------------------\n";  
		std::cout<<"Input: ";
		std::getline(std::cin, user_input);
		user_choice = check_user_input(user_input);
	}

	
	



}


