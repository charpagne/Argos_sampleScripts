# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 12:12:09 2020

@author: Arsenic
align AM 316L HT 02 dataset
"""

import numpy as np
from argos import align, process
from argos.gui import kbentry, loadtxtfile, loadimgfile, loadimgfile, msgbox
from skimage.io import imread, imsave
import cv2
from PIL import Image


msgbox("Is the DIC area fully included in the EBSD area?")

coord_ebsd = loadtxtfile("Select file containing EBSD control points")  # load EBSD points
coord_ebsd = coord_ebsd/0.4  # if points are in um, divide by step size (optional)
coord_dic = loadtxtfile("Select file containing DIC control points")  # load DIC points
nb_of_points = int(np.ma.size(coord_ebsd)/2)

degree = int(kbentry("Degree of polynomial function","degree"))  # ask polynoomial function degree
dic_map = loadimgfile("Select any DIC map")

map_init = loadimgfile("Select map to be aligned")  # load image to distort
map_name = kbentry("Output image","name")  # ask polynoomial function degree
# map_name = 'IQ'

# create distortion function according to the input parameters
distortion = align.Distortion()
distortion.findRatio(coord_dic, coord_ebsd)
distortion.find_params_from_points(coord_dic/distortion.ratio, coord_ebsd, degree)

def align_img(img,name):
    "routine to align images"
    ":: img = image to align"
    ":: save: boolean"
    "::name: string"
    img_align = process.Transform.apply_poly_distortion(img=img, transform=distortion.transform)
    # return img_align
    print("Image aligned")
    
    if len(img_align.shape) == 2: # greyscale img
        img_align = img_align[:int(dic_map.shape[0]/distortion.ratio),:int(dic_map.shape[1]/distortion.ratio)]
        cv2.imwrite('%s_align.jpg' %(name), img_align)

    if len(img_align.shape) == 3:  # rgb image
        img_align = img_align[:int(dic_map.shape[0]/distortion.ratio),:int(dic_map.shape[1]/distortion.ratio),:]
        cv2.imwrite('%s_align.jpg' %(name), img_align)


def __main__(args=None):
    align_img(map_init,map_name)
    print("Image aligned and saved")
    print("Note: for matching the grid of DIC: stretch by a ratio of %s" %(distortion.ratio))
  
    
  
if __name__ == "__main__":
    __main__()