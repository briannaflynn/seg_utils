#!/usr/bin/env python

from via import *

import json
import os
import re
from tqdm import tqdm
import numpy as np
from skimage import transform
from collections import namedtuple
from imageio import imsave, imread
import requests
from PIL import Image
from itertools import filterfalse, chain
from typing import List, Tuple, Dict
import cv2
#from . import PAGE

collection = 'beagles'
annotation_file = 'beagle_annots.json'
masks_dir = '/work/05515/bflynn/maverick2/masks'
images_dir = '/work/05515/bflynn/maverick2/images'

# Load all the data in the annotation file
# (the file may be an exported project or an export of the annotations)

def load_annotation(annotation_file: str):
    with open(annotation_file, 'r', encoding='utf8') as f:
        content = json.load(f)
    
    return content






via_data = load_annotation_data(annotation_file)

# In the case of an exported project file, you can set ``only_img_annotations=True``
# to get only the image annotations
via_annotations = load_annotation_data(annotation_file, only_img_annotations=True)
# Collect the annotated regions
working_items = collect_working_items(via_annotations, collection, images_dir)




VIAttribute = namedtuple(
    "VIAttribute", [
        'name',
        'type',
        'options'
    ]
)
VIAttribute.__doc__ = """                                                                                                                                                                                 
A container for VIA attributes.                                                                                                                                                                         
                                                                                                                                                                                                      
:param str name: The name of attribute                                                                                                                                                                    
:param str type: The type of the annotation (dropdown, markbox, ...)                                                                                                                                     
:param list options: The options / labels possible for this attribute.                                                                                                                                 
"""

def via_attributes(annotation_dict:dict, via_version:int=2):
    #print(annotation_dict.values())
    #list_attributes = list(value for value in annotation_dict['regions'].values())  # if region in value['regions'])
    #dict_attributes = {value for value in annotation_dict.values()}
    #print(dict_attributes)
    #print(list_attributes)
    
    '''
    list_attributes = [list(region['region_attributes'].keys())
                               for value in annotation_dict.values()
                               for region in value['regions']]
    
    [list(x['region_attributes'].keys()) for y in annotation_dict.values() for x in y['regions']]
    
    
    vals = {}
    for value in annotation_dict.values():
        vals = value
    print(vals)
    regions = {}
    for k, v in vals.items():
        if k == 'regions':
            regions = v
    
  
    print('regions')
    print(regions)
    print('')
    regions2 = {}
    for v in regions.values():
        regions2 = v
    print(regions2)
    
   
    print(regions2.keys())
    print('')

    for k, v in regions2.items():
        if k == 'region_attributes':
            print(v)
    
    print('')
    print(regions2)

    '''

    #WHAT IS THIS LOOKING FOR???? THE REGION ATTRIBUTE (BEAGLE) FOR EACH REGION (0 OR 1)??? HOW DO I FORMAT THIS????

    #unique_attributes = list(np.unique(list(chain.from_iterable(list_attributes))))
    
    unique_attributes = []
    unique_attributes.append("schmeagle")
    

    #dict_labels = {rgn_att: list() for rgn_att in unique_attributes}
    
    regions = {}
    for value in annotation_dict.values():
        regions = value
    
    regions_dicts = {}
    for k, v in regions.items():
        if k == 'regions':
            regions_dicts = v
    
    attributes = {}
    attributes = regions_dicts.values()
        
    
    regdict = {'region_attributes': {'label': 'Beagle'}}
    


    '''

    for region in regions:
        for k, v in region.items():
            if k == 'region_attributes':
                dict_labels[k].append(v)

    print(dict_labels)
    
    #print(dict_labels)
    '''
    dict_labels = {"label":["Schmeagle", "Beagle"]}
    
    
   # Instantiate VIAttribute objects                                                                                                                                                                       
    viattribute_list = list()
    for attribute, options in dict_labels.items():

        if all(isinstance(opt, str) for opt in options):
            viattribute_list.append(VIAttribute(name=attribute,
                                                type=None,
                                                options=list(np.unique(options))))

        elif all(isinstance(opt, dict) for opt in options):
            viattribute_list.append(VIAttribute(name=attribute,
                                                type=None,
                                                options=list(np.unique(list(chain.from_iterable(options))))))

        else:
            raise NotImplementedError
    return viattribute_list

    
    

# Collect the attributes and options                                                                                                                                                                       
list_attributes = via_attributes(via_annotations)

#print(list_attributes)


# Create one mask per option per attribute                                                                                                                                                                  
#via.create_masks(masks_dir, working_items, list_attributes, collection)



shape_attributes_dict = {}
region_dict = {}
for value in via_annotations.values():
    for v in value.values():
        #print(v)
        region_dict = v
#print(region_dict)

for item in region_dict.items():
    for k, v in enumerate(item):
#        print(k)
        print(v)
print('')
shape_att_list = []
for val in region_dict.values():
    print(val)
    shape_att_list.append(val)
    print('')

    shape_attributes_dict = val

print(shape_att_list)

label_dicts = []
for s in shape_att_list:
    for k, v in s.items():
        if k == 'region_attributes':
            label_dicts.append(v)
print(label_dicts)

labels = []
for l in label_dicts:
    for k, v in l.items():
        labels.append(v)
print(labels)
#print(shape_attributes_dict)
#print(region_dict.keys())
#print(region_dict.values())
#print(shape_attributes_dict)



practice = shape_att_list[0]

#contours = np.stack([practice['all_points_x'], practice['all_points_y'], axis=1)[:, None, :]

print(practice)
print('')
practice_list = []
for value in practice.values():
    practice_list.append(value)
print(practice_list)

x_coord = []
y_coord = []
for i in practice_list:
    for k, v in i.items():
        if k == 'all_points_x':
            x_coord.append(v)
        if k == 'all_points_y':
            y_coord.append(v)

#fp = [y for x in false_pos for y in x]

x_coord = [y for x in x_coord for y in x]
y_coord = [y for x in y_coord for y in x]

print(x_coord)
print('')
print(y_coord)

contours = np.stack((x_coord, y_coord), axis=1)
print(contours)
#vertices = np.array([[x_coord, y_coord]], dtype=np.int32)

#THIS IS JUST TO GET H AND W FOR CREATING EMPTY MASK
xy_vals = []
for wi in working_items:
    xy_vals.append(wi.original_y)
    xy_vals.append(wi.original_x)
print(xy_vals)

#THIS IS IMPORTANT, Y COMES BEFORE X

a1 = np.array([contours], dtype=np.int32)

#THIS IS JUST CREATING AN EMPTY MASK, THAT'S IT
mask = np.zeros([xy_vals[0], xy_vals[1]], np.uint8)
#print(mask)

poly_mask = cv2.fillPoly(mask, a1, 255)
print(poly_mask)

cv2.imwrite('./testimage.png', poly_mask)

print('')
print('Testing second polygon')

practice = shape_att_list[1]

practice_list =[]
for value in practice.values():
    practice_list.append(value)

print(practice_list)

x_2=[]
y_2=[]
for i in practice_list:
    for k, v in i.items():
        if k == 'all_points_x':
            x_2.append(v)
        if k == 'all_points_y':
            y_2.append(v)

x_2 = [y for x in x_2 for y in x]
y_2 = [y for x in y_2 for y in x]

contours = np.stack((x_2, y_2), axis=1)


a2 = np.array([contours], dtype=np.int32)

final_mask = cv2.fillPoly(poly_mask, a2, (66, 245, 99))
print(final_mask)

cv2.imwrite('./third_testimage.png', final_mask)

'''
def _draw_mask(via_region: dict,
               mask: np.array,
               contours_only: bool = False) -> np.array:
    """                                                                                                                                                                                                     
    :param via_region: region to draw (in VIA format)                                                                                                                                                       
    :param mask: image mask to draw on                                                                                                                                                                      
    :param contours_only: if `True`, draws only the contours of the region, if `False`, fills the region                                                                                                    
    :return: the drawn mask                                                                                                                                                                                    """

    shape_attributes_dict = via_region['shape_attributes']

    
    elif shape_attributes_dict['name'] == 'polygon':
        contours = np.stack([shape_attributes_dict['all_points_x'],
                             shape_attributes_dict['all_points_y']], axis=1)[:, None, :]

        mask = cv2.polylines(mask, [contours], True, 255, thickness=15) if contours_only \
            else cv2.fillPoly(mask, [contours], 255)

    
    return mask


'''
