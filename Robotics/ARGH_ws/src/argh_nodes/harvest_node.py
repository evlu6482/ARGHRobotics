#!/usr/bin/env python2
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
import geometry_msgs.msg
import numpy as np
from tf.transformations import quaternion_from_euler
import sys
import copy
import moveit_commander
import moveit_msgs.msg
import math
from moveit_commander.conversions import pose_to_list
import time

#creating publishing object to publish to start sensing node again
pub1 = rospy.Publisher('sensing_node_input', Bool, queue_size = 10)
#used for starting sensing node again 
data1 = True

#used for stopping harvesting node
pub2 = rospy.Publisher('coordinate_tomato', geometry_msgs.msg.Pose, queue_size = 10)
recieved_point = geometry_msgs.msg.Pose()

#used for gripper stuff
pub3 = rospy.Publisher('control_gripper', String, queue_size = 10)

#dimensions of stuff
length_gripper_open = 0.1493
length_link_2 = 0.11655
bench_height = 0.05
saftey_height = 0.025
max_angle = 135
min_angle = 90

#moving 
pose_goal = geometry_msgs.msg.Pose()

#known joint stuff
home_pos_joint = np.array([5.96377277374, -0.5757077497, -2.556312084197, -3.14978327373, -0.3186467329608,  3.139601707458496])
store_pos_joint = np.array([4.3705644607543945,-1.8971754513182582,-2.0730605125427246,-3.0040561161436976,-0.8051846663104456,3.6324658393859863])
total_height = length_link_2 + length_gripper_open + bench_height + saftey_height
vertical_harvest_height = total_height + length_link_2

def harvest_ang(tomato_height):
	global max_angle
	global min_angle
	global vertical_harvest_height
	global bench_height
	ang_dif = ( tomato_height/(vertical_harvest_height - bench_height) ) * (max_angle - min_angle) 
	
	return (-1 * max_angle) + ang_dif  


def harvest_tomatos(data):
	
	#for publishing 
	rate = rospy.Rate(2)
	robot = moveit_commander.RobotCommander()
	scene = moveit_commander.PlanningSceneInterface()
	group = moveit_commander.MoveGroupCommander("manipulator")

	planning_frame = group.get_planning_frame()
	eef_link = group.get_end_effector_link()
	group_names = robot.get_group_names()

	#only perform harvest if location is within current bounds of 1m,1m,1m = mag sqrt(3)
	if((data.position.x <= 1) and (data.position.y <= 1) and (data.position.z <= 1) ):

		#initialize global values that are in use
		global total_height
		global home_pos_joint
		global pose_goal
		global length_gripper_open
		global saftey_height
		global vertical_harvest_height
		waypoints = []

		rospy.loginfo("Tomato Location okay, beginning harvesting")
		rospy.loginfo("%f %f %f", data.position.x, data.position.y, data.position.z)
		#a bunch of edge cases for harvesting 

		#move to home and open gripper just incase
		joint_goal = group.get_current_joint_values()
		joint_goal[0] = home_pos_joint[0]
		joint_goal[1] = home_pos_joint[1]
		joint_goal[2] = home_pos_joint[2]
		joint_goal[3] = home_pos_joint[3]
		joint_goal[4] = home_pos_joint[4]
		joint_goal[5] = home_pos_joint[5]
		group.go(joint_goal, wait=True)
		group.stop()

		pub3.publish("open_fast_hard")
		rate.sleep()
		#open gripper
		if(data.position.z >= vertical_harvest_height):
			#height is above or equal to vert harvest
			
			#move down first to same x pos, y 30 cm,  same z position but -2.5 cm
			#with -90 roll
			
			#set orientation of gripper
			roll = 0
			pitch = 0
			yaw = 0
			quaternion = quaternion_from_euler(math.radians(roll), math.radians(pitch), math.radians(yaw)) #compute orientation values for gripper 

			#move to around 8 cm infront of base with orientation for harvest
			wpose = group.get_current_pose().pose
			wpose.position.y += 0.08
			start_y = wpose.position.y
			wpose.position.x = data.position.x
			wpose.position.z = data.position.z - length_gripper_open
			wpose.orientation.x = quaternion[0]
			wpose.orientation.y = quaternion[1]
			wpose.orientation.z = quaternion[2]
			wpose.orientation.w = quaternion[3]
			waypoints.append(copy.deepcopy(wpose))


			###########################################################
			#	CURRENT ERROR DONT CHANGE SAFTEY GLOBAL VARIABLE - love connor
			###########################################################

			#might start throwing this around in our codemove_group.setMaxVelocityScalingFactor(0.1);

			#move down z after orientation is reached
			wpose.position.z -= length_link_2 
			waypoints.append(copy.deepcopy(wpose))

			#move forward to tomato y location
			wpose.position.y = data.position.y + length_gripper_open - 0.005
			waypoints.append(copy.deepcopy(wpose))

			#move up to harvest tomato
			wpose.position.z += length_link_2
			waypoints.append(copy.deepcopy(wpose))

			#compute and execute path
			(plan, fraction) = group.compute_cartesian_path(waypoints,0.01,0.0)
			group.execute(plan, wait=True)

			#close gripper
			pub3.publish("close_slow_soft")
			time.sleep(5)

			#twist
			joint_goal = group.get_current_joint_values()
			joint_goal[5] = 0.0
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()
			#twist again
			joint_goal = group.get_current_joint_values()
			joint_goal[5] = -3.14
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()

			#move down aka harvest
			waypoints = []
			wpose = group.get_current_pose().pose
			wpose.position.z -= saftey_height 
			waypoints.append(copy.deepcopy(wpose))

			#translate back to original y
			wpose.position.y = start_y
			waypoints.append(copy.deepcopy(wpose))

			#compute and execute path
			(plan, fraction) = group.compute_cartesian_path(waypoints,0.01,0.0)
			group.execute(plan, wait=True)

			#move back to home
			joint_goal = group.get_current_joint_values()
			joint_goal[0] = home_pos_joint[0]
			joint_goal[1] = home_pos_joint[1]
			joint_goal[2] = home_pos_joint[2]
			joint_goal[3] = home_pos_joint[3]
			joint_goal[4] = home_pos_joint[4]
			joint_goal[5] = home_pos_joint[5]
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()

			#translate x
			waypoints = []
			wpose = group.get_current_pose().pose
			wpose.position.x += 0.40
			waypoints.append(copy.deepcopy(wpose))
			(plan, fraction) = group.compute_cartesian_path(waypoints,0.01,0.0)
			group.execute(plan, wait=True)

			#xpos to storage
			joint_goal = group.get_current_joint_values()
			joint_goal[0] = store_pos_joint[0]
			joint_goal[1] = store_pos_joint[1]
			joint_goal[2] = store_pos_joint[2]
			joint_goal[3] = store_pos_joint[3]
			joint_goal[4] = store_pos_joint[4]
			joint_goal[5] = store_pos_joint[5]
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()
			pub3.publish("open_fast_hard")
			time.sleep(3)

			#translate y and x to make moving home easier
			waypoints = []
			wpose = group.get_current_pose().pose
			wpose.position.y -= 0.02
			wpose.position.x -= 0.05 
			waypoints.append(copy.deepcopy(wpose))

			#finally move home
			joint_goal = group.get_current_joint_values()
			joint_goal[0] = home_pos_joint[0]
			joint_goal[1] = home_pos_joint[1]
			joint_goal[2] = home_pos_joint[2]
			joint_goal[3] = home_pos_joint[3]
			joint_goal[4] = home_pos_joint[4]
			joint_goal[5] = home_pos_joint[5]
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()

		elif( (data.position.z < vertical_harvest_height ) and (data.position.z > bench_height)):
			#height is below vert harvest and above table

			#move to same x pos, y 30 cm,  same z position but +2.5 cm
			#with -90 roll
			roll = harvest_ang(data.position.z)
			pitch = 0
			yaw = 0
			quaternion = quaternion_from_euler(math.radians(roll), math.radians(pitch), math.radians(yaw))
			

			adding_to_height = math.sin(abs(math.radians(roll)) - math.radians(90)) * length_gripper_open
			add_to_length = math.cos(abs(math.radians(roll)) - math.radians(90)) * length_gripper_open
			#first just move forward
			#get current pose


			wpose = group.get_current_pose().pose
			wpose.position.y += 0.03
			start_y = wpose.position.y
			wpose.position.x = data.position.x
			wpose.position.z = data.position.z + saftey_height + adding_to_height
			waypoints.append(copy.deepcopy(wpose))
			
			wpose.orientation.x = quaternion[0]
			wpose.orientation.y = quaternion[1]
			wpose.orientation.z = quaternion[2]
			wpose.orientation.w = quaternion[3]
			waypoints.append(copy.deepcopy(wpose))


			wpose.position.y = data.position.y + 0.01
			waypoints.append(copy.deepcopy(wpose))

			(plan, fraction) = group.compute_cartesian_path(waypoints,0.01,0.0)
			group.execute(plan, wait=True)


			pub3.publish("close_slow_soft")
			time.sleep(5)

			waypoints = []
			wpose = group.get_current_pose().pose
			wpose.position.z -= saftey_height 
			waypoints.append(copy.deepcopy(wpose))

			wpose.position.y = start_y
			waypoints.append(copy.deepcopy(wpose))

			(plan, fraction) = group.compute_cartesian_path(waypoints,0.01,0.0)
			group.execute(plan, wait=True)
			
			joint_goal = group.get_current_joint_values()
			joint_goal[0] = home_pos_joint[0]
			joint_goal[1] = home_pos_joint[1]
			joint_goal[2] = home_pos_joint[2]
			joint_goal[3] = home_pos_joint[3]
			joint_goal[4] = home_pos_joint[4]
			joint_goal[5] = home_pos_joint[5]
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()
			waypoints = []
			wpose = group.get_current_pose().pose
			wpose.position.x += 0.40
			waypoints.append(copy.deepcopy(wpose))
			(plan, fraction) = group.compute_cartesian_path(waypoints,0.01,0.0)
			group.execute(plan, wait=True)

			#home to storage
			joint_goal = group.get_current_joint_values()
			joint_goal[0] = store_pos_joint[0]
			joint_goal[1] = store_pos_joint[1]
			joint_goal[2] = store_pos_joint[2]
			joint_goal[3] = store_pos_joint[3]
			joint_goal[4] = store_pos_joint[4]
			joint_goal[5] = store_pos_joint[5]
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()
			pub3.publish("open_fast_hard")
			time.sleep(3)

			#storage to home
			joint_goal = group.get_current_joint_values()
			joint_goal[0] = home_pos_joint[0]
			joint_goal[1] = home_pos_joint[1]
			joint_goal[2] = home_pos_joint[2]
			joint_goal[3] = home_pos_joint[3]
			joint_goal[4] = home_pos_joint[4]
			joint_goal[5] = home_pos_joint[5]
			group.go(joint_goal, wait=True)
			group.stop()
			group.clear_pose_targets()
			#now change orientation

			# pose_goal = group.get_current_pose().pose
			# pose_goal.position
			# pose_goal.orientation.x = quaternion[0]
			# pose_goal.orientation.y = quaternion[1]
			# pose_goal.orientation.z = quaternion[2]
			# pose_goal.orientation.w = quaternion[3]

			# group.set_pose_target(pose_goal)
			# plan = group.go(wait=True)
			# group.stop()
			
			#rospy.loginfo("off")

		else:
			#height is wrong
			rospy.loginfo("Height Discrepancy")
		


		#after tomato is harvested move back a little in the y

		######################################################
		# threw in a start value for shits ang giggles
		######################################################
		pub3.publish("start")
		rate.sleep()

		#done harvesting tell sensing node to start again 
		pub1.publish(data1)
		rate.sleep()

		#reset one point value to nan to stop harvesting node
		recieved_point.position.x = 5.0
		pub2.publish(recieved_point)
		rate.sleep()


def sub_pub_harvest():
	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('sub_pub_harvest', anonymous = True)

	rospy.Subscriber("coordinate_tomato", geometry_msgs.msg.Pose, harvest_tomatos )

	rospy.spin()

if __name__ == '__main__':
	sub_pub_harvest()