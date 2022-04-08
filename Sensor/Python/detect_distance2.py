import cv2
import pyrealsense2 as rs
from definitions import *
import csv
import time
from PIL import Image

point = (0, 0)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

# Initialize Camera Intel Realsense
dc = DepthCamera()
# pc = rs.pointclou


# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)
Run=True
count=0
while Run==True:

    ret, depth_frame, color_frame = dc.get_frame()
    # Show distance for a specific point
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    distance = depth_frame[point[1], point[0]]
    RGB_at_distance = color_frame[point[1], point[0]]
    #points = rs.pointcloud
    #pc.map_to(color_frame)
    # output depth info as text file
    #with open("Output.txt", "w") as text_file:
    #    text_file.write(points)
    cv2.putText(color_frame, "{}mm".format(distance), (20,30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    cv2.putText(color_frame, "{}".format(RGB_at_distance), (20,450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    # time.sleep(2)
    count=count +1
    if count == 2000:
        Run =  False
        color_frame=cv2.cvtColor(color_frame,cv2.COLOR_BGR2RGB)
        img= Image.fromarray(color_frame)
        img.save("realsense.jpeg")
        


    if key == 27:
    
       break

'''
points = pc.calculate(depth_frame)

f = open("depth_data.txt", "a")
f.write(points)
f.close()


# open the file in the write mode
f = open('C:/Users/ecshu/Documents/ARGHRobotics/Sensor/Python/', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerow(points)

# close the file
f.close()
'''