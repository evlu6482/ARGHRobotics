#!/usr/bin/env python
# coding: utf-8

# # First go to Edit/Notebook settings and set the hardware accelerator to ```GPU```

# # Clone repo, mont drive and install dependencies

# In[ ]:


#!git clone https://github.com/victorpujolle/Tomato_detection


# # Mount google drive where dataset is stored

# # Mask R-CNN - Train on Tomato Dataset
# 
# 
# This notebook shows how to train Mask R-CNN on your own dataset.

# In[6]:


import os
import sys
import random
import math
import re
import time
import numpy as np
import cv2
import matplotlib
import matplotlib.pyplot as plt
import skimage
import itertools
import logging
import json
import re
import random
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib.patches import Polygon

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

get_ipython().run_line_magic('matplotlib', 'inline')

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


# ## Configurations

# In[7]:


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

    
    
config = TomatoConfig()
config.display()


# ## Notebook Preferences

# In[8]:


def get_ax(rows=1, cols=1, size=8):
    """Return a Matplotlib Axes array to be used in
    all visualizations in the notebook. Provide a
    central point to control graph sizes.
    
    Change the default size attribute to control the size
    of rendered images
    """
    _, ax = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    return ax


# ## Dataset
# 
# Create a synthetic dataset
# 
# Extend the Dataset class and add a method to load the shapes dataset, `load_shapes()`, and override the following methods:
# 
# * load_image()
# * load_mask()
# * image_reference()

# In[9]:


class TomatoDataset(utils.Dataset):

    def load_tomato(self, dataset_dir, subset):
        """Load a subset of the Balloon dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes. We have only one class to add.
        self.add_class("tomato", 1, "tomato")

        # Train or validation dataset?
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)

        # Load annotations
        # VGG Image Annotator (up to version 1.6) saves each image in the form:
        # { 'filename': '28503151_5b5b7ec140_b.jpg',
        #   'regions': {
        #       '0': {
        #           'region_attributes': {},
        #           'shape_attributes': {
        #               'all_points_x': [...],
        #               'all_points_y': [...],
        #               'name': 'polygon'}},
        #       ... more regions ...
        #   },
        #   'size': 100202
        # }
        # We mostly care about the x and y coordinates of each region
        # Note: In VIA 2.0, regions was changed from a dict to a list.
        annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
        annotations = list(annotations.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.
        annotations = [a for a in annotations if a['regions']]

        # Add images
        for a in annotations:
            # Get the x, y coordinaets of points of the polygons that make up
            # the outline of each object instance. These are stores in the
            # shape_attributes (see json format above)
            # The if condition is needed to support VIA versions 1.x and 2.x.
            if type(a['regions']) is dict:
                polygons = [r['shape_attributes'] for r in a['regions'].values()]
            else:
                polygons = [r['shape_attributes'] for r in a['regions']] 

            # load_mask() needs the image size to convert polygons to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "tomato",
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                width=width, height=height,
                polygons=polygons)

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a balloon dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != "tomato":
            return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance. Since we have
        # one class ID only, we return an array of 1s
        return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "tomato":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


# # Load datasets
# dataset_dir should be the path of the dataset in the drive
# 
# In this case it was created using  VGG Image Annotator (up to version 1.6) 
# 
# It saves each image in the form:
#         # { 'filename': '28503151_5b5b7ec140_b.jpg',
#         #   'regions': {
#         #       '0': {
#         #           'region_attributes': {},
#         #           'shape_attributes': {
#         #               'all_points_x': [...],
#         #               'all_points_y': [...],
#         #               'name': 'polygon'}},
#         #       ... more regions ...
#         #   },
#         #   'size': 100202
#         # }
#         # We mostly care about the x and y coordinates of each region
# 
# The dataset dir should contains 2 subfolder named ```train``` and ```val``` with the training and the validation data. 
# 
# In each of this subfolder, a file named ```via_region_data.json```
# 
# Of course you can make your own dataset class for your own dataset. 

# In[10]:


dataset_dir = r'C:\Users\Collin\OneDrive\Documents\Collin\School\Senior Year\ASEN 4018 Senior Projects\Tomato_detection\Real_dataset' #TODO Change this to your dataset directory
# Training dataset.
dataset_train = TomatoDataset()
dataset_train.load_tomato(dataset_dir, "train")
dataset_train.prepare()

# Validation dataset
dataset_val = TomatoDataset()
dataset_val.load_tomato(dataset_dir, "val")
dataset_val.prepare()


# In[11]:


# Load and display random samples
image_ids = np.random.choice(dataset_train.image_ids, 4)
for image_id in image_ids:
    image = dataset_train.load_image(image_id)
    mask, class_ids = dataset_train.load_mask(image_id)
    visualize.display_top_masks(image, mask, class_ids, dataset_train.class_names)


# ## Create Model

# In[12]:


# Create model in training mode
model = modellib.MaskRCNN(mode="training", config=config,
                          model_dir=MODEL_DIR)


# In[13]:


# Load weights trained on MS COCO, but skip layers that
# are different due to the different number of classes
# See README for instructions to download the COCO weights
init_with = "coco"

if init_with == "coco":
  model.load_weights(COCO_MODEL_PATH, by_name=True, exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", "mrcnn_bbox", "mrcnn_mask"])
elif init_with == "last":
    # Load the last model you trained and continue training
    model.load_weights(model.find_last(), by_name=True)


# ## Training
# 
# Train in two stages:
# 1. Only the heads. Here we're freezing all the backbone layers and training only the randomly initialized layers (i.e. the ones that we didn't use pre-trained weights from MS COCO). To train only the head layers, pass `layers='heads'` to the `train()` function.
# 
# 2. Fine-tune all layers. For this simple example it's not necessary, but we're including it to show the process. Simply pass `layers="all` to train all layers.

# In[ ]:


# Train the head branches
# Passing layers="heads" freezes all layers except the head
# layers. You can also pass a regular expression to select
# which layers to train by name pattern.
model.train(dataset_train, dataset_val, 
            learning_rate=config.LEARNING_RATE, 
            epochs=5, 
            layers='heads')


# In[ ]:


# Fine tune all layers
# Passing layers="all" trains all layers. You can also 
# pass a regular expression to select which layers to
# train by name pattern.
model.train(dataset_train, dataset_val, 
            learning_rate=config.LEARNING_RATE / 10,
            epochs=10, 
            layers="all")


# In[ ]:


# Save weights
# Typically not needed because callbacks save after every epoch
# Uncomment to save manually
print(MODEL_DIR)
print(os.listdir(MODEL_DIR))
model_path = os.path.join(MODEL_DIR, "mask_rcnn_tomato.h5")
model.keras_model.save_weights(model_path)


# uncomment this to save the weights in your drive
#this one takes quite a long time
#MODEL_DIR_drive = '../drive/My Drive/logs_tomato'
#model_path = os.path.join(MODEL_DIR_drive, "mask_rcnn_tomato.h5")
#model.keras_model.save_weights(model_path)


# ## Detection

# In[14]:


class InferenceConfig(TomatoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

inference_config = InferenceConfig()

# Recreate the model in inference mode
model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)

# Get path to saved weights
# Either set a specific path or find last trained weights
# model_path = os.path.join(ROOT_DIR, ".h5 file name here")
#model_path = model.find_last()
model_path = r"C:\Users\Collin\OneDrive\Documents\Collin\School\Senior Year\ASEN 4018 Senior Projects\Tomato_detection\logs\tomato20211117T2309\mask_rcnn_tomato_0005.h5"

# Load trained weights
print("Loading weights from ", model_path)
model.load_weights(model_path, by_name=True)


# In[15]:


# Test on a random image
image_id = random.choice(dataset_val.image_ids)
original_image, image_meta, gt_class_id, gt_bbox, gt_mask =    modellib.load_image_gt(dataset_val, inference_config, 
                           image_id, use_mini_mask=False)

log("original_image", original_image)
log("image_meta", image_meta)
log("gt_class_id", gt_class_id)
log("gt_bbox", gt_bbox)
log("gt_mask", gt_mask)

visualize.display_instances(original_image, gt_bbox, gt_mask, gt_class_id, 
                            dataset_train.class_names, figsize=(8, 8))


# In[17]:


results = model.detect([original_image], verbose=1)

r = results[0]
class_name=dataset_val.class_names
visualize.display_instances(original_image, r['rois'], r['masks'], r['class_ids'], 
                            dataset_val.class_names, r['scores'], ax=get_ax())


# In[33]:


myMask=r['masks']   
maskSlice=myMask[:,:,1]
import numpy
numpy.savetxt("foo.csv",maskSlice,delimiter=",")


# ## Evaluation

# In[23]:


# Compute VOC-Style mAP @ IoU=0.5
# Running on 10 images. Increase for better accuracy.
image_ids = np.random.choice(dataset_val.image_ids, 10)
APs = []
for image_id in image_ids:
    # Load image and ground truth data
    image, image_meta, gt_class_id, gt_bbox, gt_mask =        modellib.load_image_gt(dataset_val, inference_config,
                               image_id, use_mini_mask=False)
    molded_images = np.expand_dims(modellib.mold_image(image, inference_config), 0)
    # Run object detection
    results = model.detect([image], verbose=0)
    r = results[0]
    # Compute AP
    AP, precisions, recalls, overlaps =        utils.compute_ap(gt_bbox, gt_class_id, gt_mask,
                         r["rois"], r["class_ids"], r["scores"], r['masks'])
    APs.append(AP)
    
print("mAP: ", np.mean(APs))


# In[ ]:




