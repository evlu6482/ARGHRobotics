#initialize variables and load libraries
############################################################
#MaskRCNN packages
import os
import sys
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

from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log

#camera packages
import pyrealsense2 as rs
import time

from definitions import *

#set paths for project
model_path = r"C:\Users\ARGH\Documents\ARGHRobotics\Software\Tomato_MaskRCNN\Models\mask_rcnn_tomato.h5"
ImgFolder=r"C:\Users\ARGH\Documents\ARGHRobotics\Software\Tomato_MaskRCNN\Image_Exports"
mask_export_location=r"C:\Users\ARGH\Documents\ARGHRobotics\Software\Tomato_MaskRCNN\Mask_Exports"



#import and setup MaskRcnn Config 

class InferenceConfig(Config):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

inference_config = InferenceConfig()

#load a maskrcnn model in inference mod
model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=model_path)

model.load_weights(model_path, by_name=True)

#Capture Image from camera
########################################################
img=capture_image(30,False,ImgFolder)



#run detection
#######################################################
results = model.detect([img], verbose=0)
#pull masks from detection results
r = results[0]
#isolate the mask data from the detection results
myMask=r['masks']

#export the masks of tomatoes found during detection
#######################################################
Export_Masks(mask_export_location,myMask)

