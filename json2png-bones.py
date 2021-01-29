#!/usr/bin/env python

import json
import os
import random
import re
from tqdm import tqdm
import numpy as np
from collections import namedtuple
from PIL import Image
from itertools import filterfalse, chain
from typing import List, Tuple, Dict
import cv2

collection = 'Bones'
annotation_file = '/full/path/to/your/file.json'
images_dir = '/full/path/to/your/image/directory'

# parse annotation data and get the shape of the image

WorkingItem = namedtuple(
    "WorkingItem", [
        'collection',
        'image_name',
        'original_x',
        'original_y',
        'reduced_x',
        'reduced_y',
        'iiif',
        'annotations'
    ]
)    

#############################################################

# Load in a JSON File of annotations
# return a dictionary from which the mask file can be generated
# Create a tuple for metadata to pull from later
# Create a list of all tuples from JSON

#############################################################

def load_annotation_data(annotation_filename: str) -> dict:


    with open(annotation_filename, 'r', encoding='utf8') as f:
        content = json.load(f)
        
        return content
        
   
def get_working_items(via_annotations: dict, images_dir: str, collection_name: str) -> List[WorkingItem]:
   
    def _formatting(name_id: str) -> str:
        name_id = re.sub('.jpg\d*', '.jpg', name_id)
        name_id = re.sub('.JPG\d*', '.JPG', name_id)
        name_id = re.sub('.png\d*', '.png', name_id)
        return name_id

    def _get_image_shape_without_loading(filename: str) -> Tuple[int, int]:
        image = Image.open(filename)
        shape = image.size
        image.close()
        return shape

    working_items = list()

    for key, v in tqdm(via_annotations.items()):
        filename = _formatting(key)

        absolute_filename = os.path.join(images_dir, filename)
        shape_image = _get_image_shape_without_loading(absolute_filename)

        regions = v['regions']

        if regions:
            wk_item = WorkingItem(collection=collection_name,
                                  image_name=filename.split('.')[0],
                                  original_x=shape_image[0],
                                  original_y=shape_image[1],
                                  reduced_x=None,
                                  reduced_y=None,
                                  iiif=None,
                                  annotations=regions)

            working_items.append(wk_item)

    return working_items
        
## get the annotation data
via_annotations = load_annotation_data(annotation_file)

## get list of items to use later, put into a list
working_items = get_working_items(via_annotations, images_dir, collection)


#############################################################

# Begin plotting shapes from JSON 
# Organize data into a list of shape attributes dictionaries
# Organize the labels

# INPUT: Annotation data produced from the load_annotation_data function
# OUTPUT: Dictionary with two keys. 
# Key 1 - Shape attributes, Value 1 - List of shape attributes dictionaries for all shapes in an annotation file
# Key 2 - Labels, Value 2 - List of all labels in the order in which the shapes are listed in the annotation file
 

#############################################################         
        
def get_shape_attributes(via_annotation:dict):
	
	shape_attributes_dict = {}
	region_dict = {}
	shape_att_list = []
	label_dicts = []
	labels = []
	
	for v in via_annotation.values():
		for q in v.values():
			region_dict = q
			
	for val in region_dict.values():
		shape_att_list.append(val)
		shape_attributes_dict = val
		
	for s in shape_att_list:
		for k, v in s.items():
			if k == 'region_attributes':
				label_dicts.append(v)

	for l in label_dicts:
		for k, v in l.items():
			labels.append(v)
		
	polygon_dictionary = {"ShapeAttributes": shape_att_list, "Labels": labels}
	
	return polygon_dictionary
	
shape_dict = get_shape_attributes(via_annotations)

shape_att_list = shape_dict['ShapeAttributes']

		       
#############################################################

# Data should now be organized
# Return the shape information dictionary
# Extract the shape attribute list from the key "ShapeAttributes"
# Take this list and input to the mask generating function

#############################################################

def mask(shape_att_list:list, file_name:str):
	num_shapes = len(shape_att_list)
	range_shapes = [x for x in range(num_shapes)]
	
	color_list = []
	polygon_list = []
	
	for shape in range_shapes:
		p = shape_att_list[shape]
		
		p_list = []
		for value in p.values():
			p_list.append(value)
			
		x_coord = []
		y_coord = []
		
		for i in p_list:
			for k, v in i.items():
				if k == 'all_points_x':
					x_coord.append(v)
					
				if k == 'all_points_y':
					y_coord.append(v)
		
		x_coord = [y for x in x_coord for y in x]
		y_coord = [y for x in y_coord for y in x]
		
		contours = np.stack((x_coord, y_coord), axis = 1)
		
		a = np.array([contours], dtype = np.int32)
		
		c1 = random.randrange(0, 256)
		c2 = random.randrange(0, 256)
		c3 = random.randrange(0, 256)
		
		color_list.append((c1, c2, c3))

		polygon_list.append(a)
		
	xy_vals = []
	for w in working_items:
		xy_vals.append(w.original_y)
		xy_vals.append(w.original_x)
		
	zero_mask = np.zeros([xy_vals[0], xy_vals[1]], np.uint8)
	polyMask = cv2.fillPoly(zero_mask, polygon_list[0], 255)
	
	fname = file_name + ".png"
	
	polyRange = [x for x in range(1, num_shapes)]
		
	for q in polyRange:
		polyMask = cv2.fillPoly(polyMask, polygon_list[q], color_list[q])
			
	cv2.imwrite(fname, polyMask)
	
	return polyMask
	
mask(shape_att_list, "MyMask")
