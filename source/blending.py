'''
Created on Oct 13, 2013

@author: alessandro

Given two aligned images, this module perform the blending between them,
so that differences of light and gain do not produce strong discontinuities
'''

import numpy as np
import cv2

#given the height and the width of the panorama, and the barrier, that indicates
#where there is the discontinuity between the images, this function produce
#a smoothed transient in the overlapping.
#smoothing window is a parameter that determines the width of the transient
#left_biased is a flag that determines whether it is masked the left image,
#or the right one
def blending_mask(height, width, barrier, smoothing_window, left_biased=True):

    assert barrier < width

    mask = np.zeros((height, width))
    
    offset = int(smoothing_window/2)
    if left_biased:
        mask[:,barrier-offset:barrier+offset+1]=np.tile(np.linspace(1,0,2*offset+1).T, (height, 1))
        mask[:,:barrier-offset] = 1
    else:
        mask[:,barrier-offset:barrier+offset+1]=np.tile(np.linspace(0,1,2*offset+1).T, (height, 1))
        mask[:,barrier+offset:] = 1
    
    return cv2.merge([mask, mask, mask])
    
#this function apply the homography to img2 and it performs the blending while doing so
def images_blending(img1, img2, width_panorama, height_panorama, H, smoothing_window = 400):
    
    barrier = img1.shape[1] -int(smoothing_window/2)
    
    panorama1 = np.zeros((height_panorama, width_panorama, 3))
    mask1 = blending_mask(height_panorama, width_panorama, barrier, smoothing_window = smoothing_window, left_biased = True)
    panorama1[0:img1.shape[0],0:img1.shape[1],:] = img1
    panorama1 *= mask1
    
    mask2 = blending_mask(height_panorama, width_panorama, barrier, smoothing_window = smoothing_window, left_biased = False)
    panorama2 = cv2.warpPerspective(img2, H, (width_panorama, height_panorama)) * mask2
    
    return panorama1 + panorama2
    