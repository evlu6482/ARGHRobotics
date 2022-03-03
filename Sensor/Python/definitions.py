import pyrealsense2 as rs
import numpy as np
#######################################################################################################
# Author: Evan Shults
# Last edit: 03/02/2022
# 
# Code consists of a class, DepthCamera, which holds various functions 
#######################################################################################################
class DepthCamera:
    # rs2_deproject_pixel_to_point() is the main function that will outout the 3D coordinates of a given
    # x and y pixel and depth input which I am investigating
    # 
    # Inputs:
    #    - x and y: Pixel coordinate from RGB 
    #                  - this would be taken from the output of MASKrcnn code
    #    
    #    - depth: 
    #      this should be the depth info associated with the x and y pixel. need to find how to find this
    #                  - possibilites:
    #                        rs.get_frame()
    #                        depth = np.asanyarray(aligned_depth_frame.get_data())
    #                        detect_distance.py
    #    - cameraInfo:
    #       I believe this is generic info on the camera. resolution, frame size etc.
    # 
    # Outputs:
    # 
    # XYZ coordinates of the camera frame. 
    #       result[0]: x, points right
    #       result[1]: y, points down
    #       result[2]: z, points forward (away from camera)                        
    #
    def convert_depth_to_phys_coord_using_realsense(x, y, depth, cameraInfo):  
        _intrinsics = rs.intrinsics()
        _intrinsics.width = cameraInfo.width
        _intrinsics.height = cameraInfo.height
        _intrinsics.ppx = cameraInfo.K[2]
        _intrinsics.ppy = cameraInfo.K[5]
        _intrinsics.fx = cameraInfo.K[0]
        _intrinsics.fy = cameraInfo.K[4]
        #_intrinsics.model = cameraInfo.distortion_model
        _intrinsics.model  = rs.distortion.none  
        _intrinsics.coeffs = [i for i in cameraInfo.D]  
    
        result = rs.rs2_deproject_pixel_to_point(_intrinsics, [x, y], depth)  
        
        #result[0]: right, result[1]: down, result[2]: forward
        return -result[0], -result[1], result[2]

    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
                
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        if not depth_frame or not color_frame:
            return False, None, None
        return True, depth_image, color_image

    def release(self):
        self.pipeline.stop()