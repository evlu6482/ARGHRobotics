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
	#only perform harvest if real location
	if( ~(np.isnan(data.position.x) and np.isnan(data.position.y) and np.isnan(data.position.z))):
		#perform harvest
		rospy.loginfo("Begining Harvesting Sequence")
		#set recieved point values
		recieved_point.position.x = data.position.x
		recieved_point.position.y = data.position.y
		recieved_point.position.z = data.position.z

		rospy.loginfo("%f %f %f", recieved_point.position.x, recieved_point.position.y, recieved_point.position.z)
		#harvesting tomato moveit code


		# done harvesting tell sensing node to start again 
		pub1.publish(data1)
		rate.sleep()

		#reset one point value to nan to stop harvesting node
		recieved_point.position.x = float("NaN")
		pub2.publish(recieved_point)
		rate.sleep()


def sub_pub_harvest():
	rospy.init_node('sub_pub_harvest', anonymous = True)

	rospy.Subscriber("coordinate_tomato", Pose, harvest_tomatos )

	rospy.spin()

if __name__ == '__main__':
	sub_pub_harvest()