#initialize variables and load libraries
############################################################
print("#################################################################")
print("Initializing Driver Function")

#MaskRCNN packages
from ast import Num
from importlib import find_loader
from operator import truediv
import os
from pickle import FALSE, TRUE
import sys
from wsgiref.simple_server import software_version
import keras
import random
import math
import statistics
import re
import time
import tensorflow as tf
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
import skimage
import itertools
import logging
import json
import re
import numpy
import random
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib.patches import Polygon
from keras.preprocessing.image import load_img
from PIL import Image
import warnings
from matplotlib import pyplot as plt
warnings.filterwarnings('ignore', '.*do not.*', )
warnings.warn('DelftStack')
warnings.warn('Do not show this message')

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
#camera packages
import pyrealsense2 as rs
import time

from definitions import *

#matlab packages 

import matlab.engine
eng = matlab.engine.start_matlab()
real=DepthCamera()
# set paths for project
# model_path = "/home/argh/Documents/ARGHRobotics/Software/Tomato_MaskRCNN/Models/mask_rcnn_tomato.h5"
# ImgFolder="/home/argh/Documents/ARGHRobotics/Software/Tomato_MaskRCNN/Image_Exports"
# mask_export_location="/home/argh/Documents/ARGHRobotics/Software/Tomato_MaskRCNN/Mask_Exports"

model_path = r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Models\mask_rcnn_tomato.h5"
ImgFolder=r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Image_Exports"
mask_export_location=r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Mask_Exports"

# Root directory of the project
ROOT_DIR = os.path.abspath("./../")
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library 
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log
#import and setup MaskRcnn Config 
# Directory to save logs and trained model

MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
# COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# # Download COCO trained weights from Releases if needed
# if not os.path.exists(COCO_MODEL_PATH):
#     utils.download_trained_weights(COCO_MODEL_PATH)
# print("#################################################################")
print("Loading Mask Configs")
print("#################################################################")
class TomatoConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "tomato"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + tomato
 
    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 99% confidence
    DETECTION_MIN_CONFIDENCE = 0.99

    IMAGE_RESIZE_MODE = "square"
config = TomatoConfig()

# Create model in inference mode
model = modellib.MaskRCNN(mode="inference", config=config,
                          model_dir=MODEL_DIR)


class InferenceConfig(TomatoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)


# Load trained weights
model.load_weights(model_path, by_name=True)


#setup data structure for tomato data
TomatoDict = {



}


#setup conditional statements to run loop
Run=TRUE
Case="5"
Ripe_Tomato=False
harvest_target=-1   
Camera_Location="A"

#Main Execution Loop
while(Run==TRUE): #code is currently setup so that it is not interactable, comment all the "Case=" statements at the end of the blocks to turn on interactivity

    # print("----------------------------------")
    # print("Welcome to ARGH Tomato Detection")
    # print("----------------------------------")
    # print("Select Run Option")
    # print("0: Shut Down")
    # print("1: Take New Image and Detect")
    # print("2: Determine Ripeness")
    # print("3: Detect Depth")
    # print("4: Visualize Tomato")
    # print("5: Change Camera Location")
    # print("----------------------------------")
    
    # print("User Input: ",end='') #uncomment these two lines to enable interactivity
    # Case=input()

    
                
    if(Case=="0"): #end looping
        print()
        print("Shutting Down")
        Run=FALSE

    elif(Case=="1"): #image capture and tomato detection
        print()
        print("Running Image Detection")
        #run image detection
         
        #Capture Image from camera
        ########################################################
        
        ImgName="realsense.jpg" #set name for image export
        
        print("Capturing Image")
        img =real.capture_image(30,True,ImgName,ImgFolder)#run image capture function for Intel Realsense
        
        #run detection
        #######################################################
        print("Running MASK Rcnn")
        results = model.detect([img], verbose=0) #maskrcnn model detection
        #pull masks from detection results
        r = results[0]
        #isolate the mask data from the detection results
        myMask=r['masks']
        NumTomato=myMask.shape[2]

        #export the masks of tomatoes found during detection
        #######################################################
        # Export_Masks(mask_export_location,myMask) #code for exporting mask data if needed
        
        Case="2"
    elif(Case=="2"): #Ripeness Detection
        print("Detecting Ripeness")
        print() 
        print()
        count=0
        
        Ripe=[False for x in range(NumTomato)] #preinitialize array for all tomatos in scene
        
        for i in range(0, NumTomato):
            
            output=ripeness(ImgName,ImgFolder,myMask[:,:,i]) #detect ripeness on ith tomato
            Ripe[i]=output
            print("Tomato ",i, " is ripe: ", Ripe[i])
            count+=1
        

        
        for i in range(0, NumTomato): #loop through tomatoes and set first ripe tomato as harvest target
            if Ripe[i]==True:
                harvest_target=i
                Ripe_Tomato=True
                break
        if(harvest_target==-1):#if no tomatoes are ripe
            print("No Valid Harvest Target")
        else:
            print("Harvest Target Is Tomato: ", harvest_target)

        Case="3"

    elif(Case=="3"):#ellipse fitting and cartesian location detection
        if harvest_target==-1:
            print("No Valid Harvest Target")
            
        else:

            print("Getting Mask Edges")
            print()
            print()
            
            numx=len(myMask) #determine the resolution of the image
            # print(numx)
            numy=len(myMask[0])
            # print(numy)
            


            # edgeMasks = [[[0 for x in range(numx)] for y in range(numy)] for z in range(NumTomato)]

            
            mask_in=(myMask[:,:,harvest_target])#set the submask as the mask of the harvest target
            
            xpix , ypix =GetEdges(mask_in) #run get edge function to get a mask of only edges of the tomato
            xpix=matlab.double(xpix.tolist()) #change xpix and ypix into terms matlab understands
            ypix=matlab.double(ypix.tolist())

            print("Running Fit_Ellipse")#run ellipse fitting function in matlab engine
            [a,b,orientation_rad,X0,Y0,X0_in,Y0_in,long_axis,short_axis,rotated_ellipse,new_ver_line,new_horz_line]=eng.fit_ellipse(xpix,ypix,nargout=12)
            rotated_ellipse=np.asarray(rotated_ellipse) #convert variable type back to python typing
            print("Ellipse Parameters Found")


            print("Detecting Tomato Location...") #determine the centerpoint of the fit ellipse
            centerX=round(statistics.mean(rotated_ellipse[1,:]))
            centerY=round(statistics.mean(rotated_ellipse[0,:]))

            
            depth_intrin, depth = real.get_depth_intrin(centerX,centerY) #get depth data from camera
            depth_point = rs.rs2_deproject_pixel_to_point(depth_intrin, [centerX,centerY], depth) #deproject depth data into cartesian data

            #TODO need to offset for center of tomato, currently at front of tomato
            print("Location of Center Point In Camera Frame:")
            print("X: ",depth_point[0],"Y: ",depth_point[1],"Z: ", depth_point[2])
            print()

            cx,cy=calibratecamera(depth_point[0],depth_point[1],depth_point[2]) #push depth data through calibration function 
            cz=depth_point[2]

            print("Location of Calibrated Center Point In Camera Frame:")
            print("cX: ",cx,"cY: ",cy,"cZ: ", cz)
            print()
                
            print("Performing Transformation From Position ", Camera_Location)
            ax,ay,az=rotateaboutX(cx,cy,cz,Camera_Location)#Transform about x axis to move point data to arm origin
            print("Location of Center Point In Robot Frame:")
            print("X: ",ax,"Y: ",ay,"Z: ",az )
            print()

        Case="4"
    elif(Case=="4"): #image verification
        if harvest_target==-1:
            print("No Valid Harvest Target")
            
        else:
            print("Running Image Verification")
            print()
            print() 

            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert pixels from bgr to rgb
            implot = plt.imshow(image)#plot image

            # put a blue dot at (10, 20)
            center=plt.scatter(centerX,centerY,5,label='Center Point') #plot center point of ellipse
            # center.set_label('Tomatoe Center Point"')
            ellipse=plt.scatter(rotated_ellipse[1,:],rotated_ellipse[0,:],5,label='Fit Ellipse')#plot ellipse
            plt.legend(handles=[center, ellipse])#plot legends
            plt.show(block=False)
            
            plt.pause(5)#pause to hold plot open
            plt.close()
        Case="0"
        
    elif(Case=="5"):#set location for camera sensing position
        find_Location=True
        while(find_Location==True):
            print("Enter New Camera Location: A, B, or C: ")
            print()
            print() 
            Camera_Location=input()
            
            if(Camera_Location=="A" or Camera_Location=="a"):
                Camera_Location=Camera_Location.upper()
                print("Camera Located At Position ", Camera_Location)
                print()
                find_Location=False
            elif(Camera_Location=="B"or Camera_Location=="b"):
                Camera_Location=Camera_Location.upper()
                print("Camera Located At Position ", Camera_Location)
                print()
                find_Location=False
            elif(Camera_Location=="C"or Camera_Location=="c"):
                Camera_Location=Camera_Location.upper()
                print("Camera Located At Position ", Camera_Location)
                print()
                find_Location=False
            else:
                print("Incorrect Input, enter Either A, B, or C")

        Case="1"
        
    else:
        print("incorrect keyboard input")
    time.sleep(0.5)





