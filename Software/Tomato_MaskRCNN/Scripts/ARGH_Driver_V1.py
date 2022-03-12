#initialize variables and load libraries
############################################################
print("#################################################################")
print("Initializing Driver Function")

#MaskRCNN packages
from ast import Num
import os
from pickle import FALSE, TRUE
import sys
from wsgiref.simple_server import software_version
import keras
import random
import math
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

warnings.filterwarnings('ignore', '.*do not.*', )
warnings.warn('DelftStack')
warnings.warn('Do not show this message')

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
#camera packages
import pyrealsense2 as rs
import time

from definitions import *

# set paths for project
model_path = r"C:\Users\ARGH\Documents\ARGHRobotics\Software\Tomato_MaskRCNN\Models\mask_rcnn_tomato.h5"
ImgFolder=r"C:\Users\ARGH\Documents\ARGHRobotics\Software\Tomato_MaskRCNN\Image_Exports"
mask_export_location=r"C:\Users\ARGH\Documents\ARGHRobotics\Software\Tomato_MaskRCNN\Mask_Exports"

# model_path = r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Models\mask_rcnn_tomato.h5"
# ImgFolder=r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Image_Exports"
# mask_export_location=r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Mask_Exports"

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

#setup conditional statements to run loop
Run=TRUE
Case=0
while(Run==TRUE):
#Case 0: Dont Run Detection or stop detection
#Case 1: Take New Photos and Detect
#Case 2: Run Ripeness Detection
#Case 3: ...
    print("----------------------------------")
    print("Welcome to ARGH Tomato Detection")
    print("----------------------------------")
    print("Select Run Option")
    print("0: Shut Down")
    print("1: Take New Image and Detect")
    print("2: Determine Ripeness")
    print("3: Move Camera To New Environment")
    print("4: Push Movement Commands To UR10e")
    print("----------------------------------")
    
    print("User Input: ",end='') 
    Case=input()


            
    if(Case=="0"):
        print()
        print("Shutting Down")
        Run=FALSE

    elif(Case=="1"):
        print()
        print("Running Image Detection")
        #run image detection
         
        #Capture Image from camera
        ########################################################
        try:
            ImgName="realsense.jpg"
            img=capture_image(30,True,ImgName,ImgFolder)
            #run detection
            #######################################################
            results = model.detect([img], verbose=0)
            #pull masks from detection results
            r = results[0]
            #isolate the mask data from the detection results
            myMask=r['masks']
            NumTomato=myMask.shape[2]

            #export the masks of tomatoes found during detection
            #######################################################
            Export_Masks(mask_export_location,myMask)
        except:
            print("ERROR: Not able to capture image")
            print()

    elif(Case=="2"):
        print("Detecting Ripeness")
        print() 
        print()
        count=0
        
        Ripe=[False for x in range(NumTomato)]
        
        for i in range(0, NumTomato):
            
            output=ripeness(ImgName,ImgFolder,myMask[:,:,i])
            Ripe[i]=output
            print("Tomato ",i, " is ripe: ", Ripe[i])
            count+=1
            print(count)
        

    elif(Case=="3"):
        print("Not Implimented Yet")
        print()
        print()
    elif(Case=="4"):
        print("Not Implimented Yet")
        print()
        print() 
    else:
        print("incorrect keyboard input")
    time.sleep(0.5)





