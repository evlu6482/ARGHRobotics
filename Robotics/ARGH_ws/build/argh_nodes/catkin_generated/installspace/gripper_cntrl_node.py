#!/usr/bin/env python2
import rospy              
from std_msgs.msg import String                                  
import socket      
import time       
                            
                            
host = '192.168.0.12'     
port = 54321              
                            
def grip_some_tomatos(data):                                     
  if(data.data == 'close'):                                    
    formatted = '091003E8000306090000FFFFFF4229'.decode('hex')
  if(data.data == 'open'):                                   
    formatted = '091003E800030609000000FFFF7219'.decode('hex')
  if(data.data == 'start'):                                  
    formatted = '091003E800030601000000000072E1'.decode('hex')
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  s.connect((host,port))
  s.sendall(formatted)  
  data = s.recv(1024)   
  s.close 
  

                            
                            
def sub_grip():           
  rospy.init_node('sub_grip', anonymous=True)                  
                          
  rospy.Subscriber("control_gripper",String, grip_some_tomatos)
  rospy.spin()     

if __name__ == '__main__':
  sub_grip()                                                                                   
