#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Apr 16, 2013

@author: alessandro
'''
import numpy as np
import cv2

def getsize(img):
    h, w = img.shape[:2]
    return w, h

class image_alignment(object):
    
    SIFT = 0
    SURF = 1
    ORB = 2     #should be used just with BF MATCHER (uint8 descriptor)
    BRISK = 3
    
    FLANN = 0
    BFMATCHER = 1

    
    def __init__(self, feat_type=SIFT, matcher_type=FLANN, params = None):
        
        self.detector, norm = self.features_detector(feat_type=feat_type, params = params)
        self.matcher = self.features_matcher(matcher_type=matcher_type, norm=norm)
    
    
    def features_detector(self, feat_type = SIFT, params = None):
        
        assert feat_type == self.SIFT or feat_type == self.SURF or \
            feat_type == self.ORB or feat_type == self.BRISK
        
        if feat_type == self.SIFT:
            
            if params is None:
                nfeatures = 0
                nOctaveLayers = 3
                contrastThreshold = 0.04
                edgeThreshold=10
                sigma=1.6
            else:
                nfeatures = params["nfeatures"]
                nOctaveLayers = params["nOctaveLayers"]
                contrastThreshold = params["contrastThreshold"]
                edgeThreshold = params["edgeThreshold"]
                sigma = params["sigma"]
            
            detector = cv2.SIFT(nfeatures=0, 
                                nOctaveLayers=3, contrastThreshold=0.04, 
                                edgeThreshold=10, sigma=1.6)
            norm = cv2.NORM_L2
        elif feat_type == self.SURF:
            
            if params is None:
                hessianThreshold = 3000
                nOctaves = 1
                nOctaveLayers = 1
                upright = True
                extended = False
            else:
                hessianThreshold = params["hessianThreshold"]
                nOctaves = params["nOctaves"]
                nOctaveLayers = params["nOctaveLayers"]
                upright = params["upright"]
                extended = params["extended"]
                
            detector = cv2.SURF(hessianThreshold = hessianThreshold, 
                                nOctaves = nOctaves, 
                                nOctaveLayers = nOctaveLayers, 
                                upright = upright, 
                                extended = extended)
            norm = cv2.NORM_L2
            
        elif feat_type == self.ORB:
            detector = cv2.ORB(nfeatures=8000, scaleFactor=1.1, nlevels=8, edgeThreshold=10, firstLevel=0, WTA_K=2, patchSize=10)
            norm = cv2.NORM_HAMMING
        elif feat_type == self.BRISK:
            detector = cv2.BRISK()
            norm = cv2.NORM_HAMMING
       
        return detector, norm
    
    
    def features_matcher(self, matcher_type = FLANN , norm = cv2.NORM_L2 ):
        
        FLANN_INDEX_KDTREE = 1  # opencv bug: flann enums are missing
        FLANN_INDEX_LSH    = 6
        
        if matcher_type==self.FLANN:
            if norm == cv2.NORM_L2:
                flann_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            else:
                flann_params= dict(algorithm = FLANN_INDEX_LSH,
                               table_number = 6, # 12
                               key_size = 12,     # 20
                               multi_probe_level = 1) #2
            matcher = cv2.FlannBasedMatcher(flann_params, {})  # bug : need to pass empty dict (#1329)
        else:
            matcher = cv2.BFMatcher(norm)
        
        return matcher
    
    
    def filter_matches(self, kp1, kp2, matches, ratio = 0.75):
        
        mkp1, mkp2 = [], []
        
        for m in matches:
            
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                m = m[0]
                mkp1.append( kp1[m.queryIdx] )
                mkp2.append( kp2[m.trainIdx] )
                
        p1 = np.float32([kp.pt for kp in mkp1])
        p2 = np.float32([kp.pt for kp in mkp2])
        kp_pairs = zip(mkp1, mkp2)
        
        return p1, p2, kp_pairs
    
    
    def get_homography(self, img1, img2, mask1=None, mask2=None):
                        
        kp1, desc1 = self.detector.detectAndCompute(img1, None)
        kp2, desc2 = self.detector.detectAndCompute(img2, None)
        
        raw_matches = self.matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2)
        p1, p2, kp_pairs = self.filter_matches(kp1, kp2, raw_matches)
        if len(p1) >= 4:
            H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
            
            return H, status
        else:
            return None, None
    
    
    def align(self, img1, img2, mask1=None, mask2=None):
                
        H, status = self.get_homography(img2, img1, mask2, mask1)
            
        if H is None:
            return None, None, None # img1, img2, H
        
        img2_aligned = cv2.warpPerspective(img2.Image, H, getsize(img2.Image))
        
        assert img2_aligned is not None
        
        return img1, img2_aligned, H
        