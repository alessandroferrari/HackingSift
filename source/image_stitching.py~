'''
Created on Apr 26, 2013

@author: alessandro
'''
from image_alignment import image_alignment
from blending import images_blending
import numpy as np
import cv2
import os

fn_base = os.path.join(os.getcwd(),"test_images")
#edit here for trying with different images
fn_img1 = "rockfeller_1.JPG"
fn_img2 = "rockfeller_2.JPG"

#reading images
img1 = cv2.imread(os.path.join(fn_base, fn_img1))
img2 = cv2.imread(os.path.join(fn_base, fn_img2))

height_img1 = img1.shape[0]
width_img1 = img1.shape[1]
nch_img1 = img1.shape[2]
#watch out: coordinates in opencv are inverted compared to numpy!
img1 = cv2.resize(img1, (width_img1/2, height_img1/2))

height_img2 = img2.shape[0]
width_img2 = img2.shape[1]
nch_img2 = img2.shape[2]
img2 = cv2.resize(img2, (width_img2/2, height_img2/2))

assert nch_img1 == nch_img2

height_panorama = height_img1 / 2
width_panorama = width_img1  

#sift parameters
sift_params = dict()
#number of features, if 0, the number will be determined according to the other 
#parameters
sift_params["nfeatures"] = 0
sift_params["nOctaveLayers"] = 3
#the higher the threshold, the strongest features are kept, while the other
#are discarded
sift_params["contrastThreshold"] = 0.04
sift_params["edgeThreshold"] = 10
#sigma of the blurring gaussian kernel used for smoothing when building the
#pyramid
sift_params["sigma"] = 1.6

#creating the instance of the image aligner
img_align = image_alignment(feat_type = image_alignment.SIFT, params = sift_params)
#designing the homography matrix by detecting matches between features in the
#two images
#sift features computation -> flann (approximate nearest neighbours) -> ransac for outliers removal
H, status = img_align.get_homography(img2, img1)
#apply the homography for overlapping images, meanwhile performing blending between
#them
panorama_image = images_blending(img1, img2, width_panorama, height_panorama, H)

#saving the panorama image
cv2.imwrite(os.path.join(fn_base,"panorama.jpg"), panorama_image)


