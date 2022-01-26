import cv2
import pyrealsense2
from realsense_depth import *


'''
def show_distance(event, x, y, args, params):
    global point
    point = (x, y)
'''

def show_distance(event, x, y, params):
    global Point
    Point = (x, y)
    

# Initialize Camera Intel Realsense
dc = DepthCamera()

# Mouse and depth information display:
cv2.namedWindow("Color Frame")
cv2.setMouseCallback("Color Frame", show_distance)


while True:
    ret, depth_frame, color_frame = dc.get_frame()

    # Show Distance at specific point:
 
    cv2.circle(color_frame, Point, 4, (0, 0, 255)) # circle on the picture at random point
    dist_at_Point = depth_frame[Point[1],Point[0]]

    print(dist_at_Point)


    cv2.imshow('Depth Frame', depth_frame)
    cv2.imshow("Color Frame", color_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break






'''
# Create mouse event
cv2.namedWindow("Color frame")
cv2.setMouseCallback("Color frame", show_distance)

while True:
    ret, depth_frame, color_frame = dc.get_frame()

    # Show distance for a specific point
    cv2.circle(color_frame, point, 4, (0, 0, 255))
    distance = depth_frame[point[1], point[0]]

    cv2.putText(color_frame, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

    '''