#!/usr/bin/env python2

import rospy
import os
import numpy as np
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose


pub_sense = rospy.Publisher('sensing_node_input',Bool,queue_size = 10) # reset node
pub_move = rospy.Publisher('sensing_node_boolean_move',Bool, queue_size= 10)
pub_geom = rospy.Publisher('coordinate_tomato',Pose, queue_size = 10)
Camera_Location = 1
script_location = "/home/argh/Documents/ARGHRobotics/Software/Tomato_MaskRCNN/Scripts/Main"
coord_file = "/home/argh/Documents/ARGHRobotics/Software/Tomato_MaskRCNN/Mask_Exports/Coordinates.csv"

def sense_callback(data):
    rate = rospy.Rate(2)
    if(data.data==True):
        #RUN SCRIPT
        rospy.loginfo("Beginning Sensing")

        # create csv with camera location
        np
        # write Camera_Location to text file
        os.path.join(script_location)
        os.system("conda run -n maskrcnn python -Wignore ARGH_Driver_V1.py")
        tomato_found = os.path.exists(coord_file)
        if(tomato_found):
            coords = np.loadtxt(coord_file)
            geometry = Pose()
            geometry.position.x = coords[0]
            geometry.position.y = coords[1]
            geometry.position.z = coords[2]
            pub_geom.publish(geometry)
            rate.sleep()
        else:
            pub_move.publish(Bool(True))
            if(Camera_Location==3):
                Camera_Location=1
            else:
                Camera_Location=Camera_Location+1
            rate.sleep()
            rospy.loginfo("No tomato found, moving sensor position")
        pub_sense.publish(Bool(False))
        rate.sleep()

# need to change to an async spin for reasons?
def sense_node():
    rospy.init_node('sense_node',anonymous=True)
    rospy.Subscriber('sensing_node_input',Bool,sense_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        sense_node()
    except rospy.ROSInterruptException:
        pass
