import cv2
import pip
import pyrealsense2 as rs
from definitions import *
import csv
import time



x = 77
y = 152

point = (x, y)

dc = DepthCamera()

ret, depth_frame, color_frame = dc.get_frame()

depth = int(depth_frame[point[1], point[0]])


print("depth = ",depth)
# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams

pipeline.start()
profile = pipeline.get_active_profile()
print("profile = ", profile)
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
print("depth_profile = ", depth_profile)
depth_intrinsics = depth_profile.get_intrinsics()
print("depth_intrinsics = ", depth_intrinsics)
w, h = depth_intrinsics.width, depth_intrinsics.height
print("w,h =" , w,h)




cameraInfo = [640, 480, 324.399, 243.36, 385.76, 385.76 ]
# print()
# 
# print("camera info= ", cameraInfo)
# result = rs.rs2_deproject_pixel_to_point(cameraInfo, [x, y], depth)  

# print(result[0], result[1], result[2])

dc.convert_depth_to_phys_coord_using_realsense(x, y, depth, cameraInfo)

# print(result[0], result[1], result[2])