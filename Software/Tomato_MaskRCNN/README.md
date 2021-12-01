# Mask R-CNN for object instance segmentation

This is an implementation of [Mask R-CNN](https://arxiv.org/abs/1703.06870) on Python 3, Keras, and TensorFlow.
The model generates bounding boxes and segmentation masks for each instance of an object in the image.
It's based on Feature Pyramid Network (FPN) and a ResNet101 backbone.

The repository provide on a simple implementation of the Mask R-CNN built on FPN
and ResNet101 and a Jupyter notebooks to train the network on a custom dataset using google colab using pretrained weights
It was created to detect tomatoes on an image, but it can be easily repurposed and trained.

# Tomato folder
* ```Detect_Image``` is the main script
* ```Tomato.py``` provides classes needed to configure the model
* ```visualize.py``` provides functions needed to visualize inferences
* ```train_tomato.ipynb``` is a jupyter notebook usable to train the network using google colab

# Tomato dataset
I made a small dataset for tomato detection. pLease feel free to use it
# Training on your own dataset


To  train on your own dataset you need to extend two classes:

* ```Config``` This class contains the default configuration. Subclass it and modify the attributes you need to change.
* ```Dataset```  This class provides a consistent way to work with any dataset. It allows you to use new datasets for training without having to change the code of the model.
It also supports loading multiple datasets at the same time, which is useful if the objects you want to detect are not all available in one dataset.


# Create your own dataset without having to write new code

You can search images on flickr, limiting the licence type to Commercial use & mods allowed. Between 75 and 100 images should be enough. You may need more images if you need very good accuracy
but in simple cases it will be enough because we use transfert learning, meaning we don't train the model from scratch but start with a weight file that’s been trained on the COCO dataset.

Then divide them into a training set and a validation set, named ```train``` and ```val```.

There is a lot of tools to annotate images. The code here is made for [Via (VGG image annotator)](http://www.robots.ox.ac.uk/~vgg/software/via/).
It’s a single HTML file that you download and open in a browser.

Then you can annotate your images, using only the polygon annotation tool (you can use other tools but you'll have to extend the ```Dataset``` class)
Save the annotation using the JSON file,  each mask is a set of polygon points.
You should create 2 JSON files, for the training and the validation set. The name of the file should be ```via_region_data.json```.

Then, upload your dataset on your google drive and go on google colab.

# Installation Instructions

Step By Step Mask RCNN Installation
Attention❗️

Compatible Python Version: python==3.6.12

IDE: Anaconda Cloud & Conda Prompt

-Anaconda Cloud: https://www.anaconda.com

🔺 Step 1: Compatible with Python 3.6 version, a virtual environment named maskrcnn is created in conda prompt.

conda create -n maskrcnn python=3.6.12

🔺 Step 2: The maskrcnn virtual environment is activated.

conda activate maskrcnn

🔺 Step 3: Mask RCNN must be installed in the requirements.txt file located in the GitHub store. The requirements.txt file will load the libraries needed for your project in batch.

pip install -r requirements.txt

Dependencies

numpy, scipy, cython, h5py, Pillow, scikit-image, tensorflow==1.3 keras==2.0.8, jupyter

For GPU: tensorflow-gpu:1.15.0, keras:2.0.8 For CPU: tensorflow:1.14.0, keras:2.0.8, h5py:2.10.0

numpy
scipy
Pillow
cython
matplotlib
scikit-image
tensorflow-gpu==1.15.0 --> replace this with tensorflow:1.14.0 for cpu support
keras==2.0.8
opencv-python
h5py==2.10
imgaug
IPython[all]

🔺 Step 3.5: Installing CUDA For running on a gpu (only needed if running on a gpu)
Install CUDA 10.2
https://developer.nvidia.com/cuda-10.2-download-archive


Download cuDNN v8.3.1 (November 22nd, 2021), for CUDA 10.2
https://developer.nvidia.com/rdp/cudnn-download

Navigate to the location of the cuda install, for me this is located at 
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v10.2

open the downloaded cuDNN file

drag and drop the contents of  bin, include and lib from cuDNN into the same folder names inside of your CUDA installation

🔺 Step 4: Running the setup.py file.

python setup.py install




