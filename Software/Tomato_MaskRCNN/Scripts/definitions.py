from turtle import end_fill
import pyrealsense2 as rs
import numpy as np
import cv2
import time
from PIL import Image
import os
import keras
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



#Functions and classes added by Collin Rasbid:

#function to convert image to array, used in manual jpg conversion
def img_to_array(img, data_format='channels_last', dtype='float32'):
    """Converts a PIL Image instance to a Numpy array.
    # Arguments
        img: PIL Image instance.
        data_format: Image data format,
            either "channels_first" or "channels_last".
        dtype: Dtype to use for the returned array.
    # Returns
        A 3D Numpy array.
    # Raises
        ValueError: if invalid `img` or `data_format` is passed.
    """
    if data_format not in {'channels_first', 'channels_last'}:
        raise ValueError('Unknown data_format: %s' % data_format)
    # Numpy array x has format (height, width, channel)
    # or (channel, height, width)
    # but original PIL image has format (width, height, channel)
    x = np.asanyarray(img, dtype=dtype)
    if len(x.shape) == 3:
        if data_format == 'channels_first':
            x = x.transpose(2, 0, 1)
    elif len(x.shape) == 2:
        if data_format == 'channels_first':
            x = x.reshape((1, x.shape[0], x.shape[1]))
        else:
            x = x.reshape((x.shape[0], x.shape[1], 1))
    else:
        raise ValueError('Unsupported image shape: %s' % (x.shape,))
    return x

#function to capture an image from the intelrealsense camera
def capture_image(NumFrames:int,Save_Img:bool,Img_Name:str,ImgFolder:str):
    #inputs:
        #NumFrames: Int, Number of frames to  stream before capturing image
        #Save_Img: Bool, True/False - true to save the final image to a location on the drive
        #ImgFolder: str, directory Location to save an image to
        
    #outputs:
        #img: 3 dimensional array with the rgb values of the captured image
   # Initialize Camera Intel Realsense 
    point = (0, 0)
    dc = DepthCamera()  

    # Create mouse event
    cv2.namedWindow("Color frame")
    # cv2.setMouseCallback("Color frame", show_distance)
    Run=True
    count=0

    while Run==True:
        #grab frames from intel realsense
        ret, depth_frame, color_frame = dc.get_frame()
        
        
    
        # RGB_at_distance = color_frame[point[1], point[0]]
    
        
        # cv2.putText(color_frame, "{}".format(RGB_at_distance), (20,450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        cv2.imshow("Color frame", color_frame)
        key = cv2.waitKey(1)
        #time.sleep(.5)
        count=count +1
        if count == NumFrames:
            Run = False
            os.chdir(ImgFolder)
            img=cv2.cvtColor(color_frame,cv2.COLOR_BGR2RGB)
            
            if Save_Img:
                img_save= Image.fromarray(img)
                img_save.save(Img_Name)

    
    return img

def Export_Masks(mask_export_location:str, myMask):
    #clean directory of previously created masks
    os.chdir(mask_export_location)    
    for f in os.listdir(mask_export_location):
     os.remove(os.path.join(mask_export_location, f))


    num_masks=myMask.shape[2]
    print("number of masks:",num_masks)
    for i in range(0,num_masks):
        maskSlice=myMask[:,:,i]
        np.savetxt("Mask"+ str(i),maskSlice,delimiter=",")
        print("adding ", "Mask",str(i), " to directory")

    return


def ripeness(Img_Name:str,ImgFolder,mask):
    
    # read in image from file
    # singleTomato = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
    os.chdir(ImgFolder)
    
    img = cv2.imread(Img_Name,cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    numx=len(img)
    numy=len(img[0])

    Black_array=np.zeros((numx,numy,3))

    singleTomato=img
    numPixelTomato=0
# for i=1:x
#    for j=1:y
#      if M1(i,j)~= 1  %If pixel in image is not in the mask, color pixel grey 
#         image(i,j,:)= I(i,j,:);
#      end  
#    end
# end
    dispimg=Image.fromarray(singleTomato,'RGB')
    dispimg.show()
    for x in range(numx):
        for y in range(numy):
            # print(x," ",y)
            
            if(mask[x,y] != 1):
                singleTomato[x,y,0]=Black_array[x,y,0]
                singleTomato[x,y,1]=Black_array[x,y,1]
                singleTomato[x,y,2]=Black_array[x,y,2]

            else:
                numPixelTomato+=1
                

    # dispimg=Image.fromarray(singleTomato,'RGB')
    # dispimg.show()



    # change to black/white for pixel counting 
    # gray = cv2.cvtColor(singleTomato, cv2.COLOR_RGB2GRAY)
    # dispimg=Image.fromarray(gray)
    # dispimg.show()
    # calculate total non-black pixels from first mask

    # find total pixels within image returned

    # since mask turns all non-tomato pixels black, count all non-black pixels
    # numPixelTomato = cv2.countNonZero(gray)

    print("Total Tomato Pixels: ",numPixelTomato)

    # convert to hsv
    hsvImg = cv2.cvtColor(singleTomato, cv2.COLOR_RGB2HSV)
    
    # define hsv cuttoffs from research paper
    weaker1 = np.array([0,43,46])
    stronger1 = np.array([10,255,255])
    weaker2 = np.array([156,43,46])
    stronger2 = np.array([180,255,255])

    # create masks using cutoffs
    mask1 = cv2.inRange(hsvImg,weaker1,stronger1)
    mask2 = cv2.inRange(hsvImg,weaker2,stronger2)

    # concatenate masks to create one mask
    maskRed = mask1 | mask2

    # calculate total non-black pixels from red mask
    numPixelRed = cv2.countNonZero(maskRed)
    print("Red pixels: ", numPixelRed)

    # calculate ripeness ratio
    ripenessRatio = numPixelRed/numPixelTomato

    print("Ripeness Ratio: ", ripenessRatio)
    
    # assign whether or not tomato is ripe
    if ripenessRatio >= 0.5:
        ripeScore = True # tomato is deemed ripe    
    else:
        ripeScore = False # tomato is deemed unripe


    # singleTomato=img
    # dispimg=Image.fromarray(img,'RGB')
    # dispimg.show()

    return(ripeScore)

def GetEdges(Mask):

    [numx,numy]=np.shape(Mask)
    # numx=int(len(Mask))
    # numy=int(len(Mask[0]))

    EdgeMask= np.zeros((numx,numy))

    for x in range(0,numx-1):
        # print(x)
        for y in range(0,numy-1):
            # print(y)
            if(x==0 or y==0):
                if (Mask[x,y] == True):
                    EdgeMask[x,y] = 1  
                    # print("Edge") 
            elif(x == numx-1 or y== numy-1):
                if (Mask[x,y] == True):
                    EdgeMask[x,y] = True
                    # print("Edge")
            elif( Mask[x,y]==True and (( Mask[x-1,y] ==False ) or ( Mask[x+1,y] ==False ) )):
                    EdgeMask[x,y]=True
                    # print("Edge")
            elif( Mask[x,y]==True and (( Mask[x,y-1] ==False ) or ( Mask[x,y+1] ==False ) )):
                    EdgeMask[x,y]=True
                    # print("Edge")


    edgeArr=np.argwhere(EdgeMask > 0)

    xpix= edgeArr[:,0]
    ypix= edgeArr[:,1]



    return(xpix,ypix)


def getCenterpoint():





    return()