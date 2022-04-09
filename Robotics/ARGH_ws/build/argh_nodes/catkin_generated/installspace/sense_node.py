#!/usr/bin/env python2

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose

pub_sense = rospy.Publisher('sensing_node_input',Bool,queue_size = 10) # reset node
pub_move = rospy.Publisher('sensing_node_boolean_move',Bool, queue_size= 10)
pub_geom = rospy.Publisher('coordinate_tomato',Pose, queue_size = 10)

def callback(data):
    rate = rospy.Rate(2)
    if(data.data==True):
        #run script
        rospy.loginfo("Beginning Sensing")

        #dummy values
        tomato_found = False
        geometry = Pose()
        geometry.position.x = 0
        geometry.position.y = 0
        geometry.position.z = 0

        if(tomato_found):
            pub_geom.publish(geometry)
            rate.sleep()
        else:
            pub_move.publish(Bool(True))
            rate.sleep()
            rospy.loginfo("No tomato found, moving sensor position")
        pub_sense.publish(Bool(False))
        rate.sleep()

def sense_node():
    rospy.init_node('sense_node',anonymous=True)
    rospy.Subscriber('sensing_node_input',Bool,callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        sense_node()
    except rospy.ROSInterruptException:
        pass