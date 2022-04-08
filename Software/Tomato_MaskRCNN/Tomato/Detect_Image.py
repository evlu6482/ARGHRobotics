#initialize variables and load libraries
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

#camera packages
import pyrealsense2 as rs
from definitions import *
import time



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

# Root directory of the project
ROOT_DIR = os.path.abspath("./../")
print(os.listdir(ROOT_DIR))
# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn.model import log


# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


## Set Detection Congfigs

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
config.display()


#set notebook preferences
def get_ax(rows=1, cols=1, size=8):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Change the default size attribute to control the size
    of rendered images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax


# Create model in inference mode
model = modellib.MaskRCNN(mode="inference", config=config,
                          model_dir=MODEL_DIR)


# Detection code
class InferenceConfig(TomatoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)

# set paths to important directories
model_path = r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Models\mask_rcnn_tomato.h5"
ImgFolder=r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Image_Exports"
mask_export_location=r"C:\Users\crasb\Documents\ARGH\ARGHRobotics\Software\Tomato_MaskRCNN\Mask_Exports"


# Load trained weights
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)

#set image for detection

# load photograph for detection
#os.chdir(ImgFolder)
#img = load_img('test1.jpg')
#img = img_to_array(img)


#camera stuff


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
    
  
    RGB_at_distance = color_frame[point[1], point[0]]
  
    
    cv2.putText(color_frame, "{}".format(RGB_at_distance), (20,450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    
    cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    time.sleep(.5)
    count=count +1
    if count == 3:
        Run = False
        os.chdir(ImgFolder)
        img=cv2.cvtColor(color_frame,cv2.COLOR_BGR2RGB)
        
        img_save= Image.fromarray(img)
        img_save.save("realsense.jpeg")


    if key == 27:
    
       break



#run detection
results = model.detect([img], verbose=0)
#pull masks from detection results
r = results[0]


#set class names 
#class_names=['BG','tomato']
#visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], 
#                            class_names, r['scores'], ax=get_ax())




#Exporting mask into csv data 
os.chdir(mask_export_location)    
for f in os.listdir(mask_export_location):
    os.remove(os.path.join(mask_export_location, f))

MaskName="Mask_"
myMask=r['masks']

num_masks=myMask.shape[2]
print(num_masks)
for i in range(0,num_masks):
    maskSlice=myMask[:,:,i]
    numpy.savetxt(MaskName+ str(i),maskSlice,delimiter=",")
    print("adding ", MaskName,str(i), " to directory")





