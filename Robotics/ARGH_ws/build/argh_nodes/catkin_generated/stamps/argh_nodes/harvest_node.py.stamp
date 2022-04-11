#!/usr/bin/env python2
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose
import numpy as np


#creating publishing object to publish to start sensing node again
pub1 = rospy.Publisher('sensing_node_input', Bool, queue_size = 10)
#used for starting sensing node again 
data1 = True

#used for stopping harvesting node
pub2 = rospy.Publisher('coordinate_tomato', Pose, queue_size = 10)
recieved_point = Pose()

def harvest_tomatos(data):
	
	#for publishing 
	rate = rospy.Rate(2)

	#only perform harvest if location is within current bounds of 1m,1m,1m = mag sqrt(3)
	
	if((data.position.x <= 1) and (data.position.y <= 1) and (data.position.z <= 1) ):
		rospy.loginfo("Tomato Location okay, beginning harvesting")

		#a bunch of edge cases for harvesting 

		rospy.loginfo("%f %f %f", data.position.x, data.position.y, data.position.z)












		#after tomato is harvested move back a little in the y


		#done harvesting tell sensing node to start again 
		#pub1.publish(data1)
		#rate.sleep()

		#reset one point value to nan to stop harvesting node
		recieved_point.position.x = 5.0
		pub2.publish(recieved_point)
		rate.sleep()


def sub_pub_harvest():
	rospy.init_node('sub_pub_harvest', anonymous = True)

	rospy.Subscriber("coordinate_tomato", Pose, harvest_tomatos )

	rospy.spin()

if __name__ == '__main__':
	sub_pub_harvest()