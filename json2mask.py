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

#annotation_file = '/path/to/your.json'
#images_dir = '/path/to/your/images'
#output_filename = 'MyMask'

class Mask:

#############################################################

# __init__
# Load in a JSON File of annotations
# return a dictionary from which the mask file can be generated
# You can also opt to input your own annotation dict (ideal for iterating on multiple annotations)

#############################################################

	def __init__(self, annotation_file, images_dir=None, file_name=None,  annotation_dict=None):
		
		
		self.annotation_file = annotation_file
		self.images_dir = images_dir
		self.file_name = file_name
		
		if annotation_dict is None:
			
			def load_annots(annotation_file):
				with open(annotation_file, 'r', encoding = 'utf8') as f:
					content = json.load(f)
				
					return content
				
			self.annotation_dict = load_annots(annotation_file)
			
		else:
		
			self.annotation_dict = annotation_dict
		
		
		for key, v in tqdm(self.annotation_dict.items()):
				filename = key
				absolute_img_filename = os.path.join(images_dir, filename)
			
				image = Image.open(absolute_img_filename)
				shape = image.size
				image.close()
				shapes = shape
				
		self.shapes = shapes
		
		self.absolute_img_filename = absolute_img_filename
		
		## This makes it private to the class, declare in here if you want to change these values per instantiation of the class
	
	
# annotation dictionary converted from the JSON annotation input file
	
	def annotDict(self):
		annot_dict = self.annotation_dict
		return annot_dict
		
# check the shapes; organize by x and y 
	
	def getShapes(self):
	
		shapeDict = {"x": self.shapes[0], "y": self.shapes[1]}
		
		return shapeDict
			
#############################################################

# Begin plotting shapes from JSON 
# Organize data into a list of shape attributes dictionaries
# Organize the labels

# INPUT: Annotation data produced from the load_annotation_data function
# OUTPUT: Dictionary with two keys. 
# Key 1 - Shape attributes, Value 1 - List of shape attributes dictionaries for all shapes in an annotation file
# Key 2 - Labels, Value 2 - List of all labels in the order in which the shapes are listed in the annotation file
 

#############################################################  
			
	def get_shape_attributes(self):
		shape_attributes_dict = {}
		region_dict = {}
		shape_att_list = []
		label_dicts = []
		labels = []
		
		for v in self.annotation_dict.values():
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
		
#############################################################

# Data should now be organized
# Return the shape information dictionary
# Extract the shape attribute list from the key "ShapeAttributes"
# Take this list and input to the mask generating function
# Full mask pipeline, from image and annotation file to mask.png file
# Input: annotation file, image directory, and specified output file name
# Output: mask file in png format 

#############################################################

	def drawMask(self):
		
		region_dict = {}
		shape_att_list = []
		
		
		for v in self.annotation_dict.values():
			for q in v.values():
				region_dict = q
				
		for val in region_dict.values():
			shape_att_list.append(val)
			
		num_shapes = len(shape_att_list)
		range_shapes = [x for x in range(num_shapes)]
		
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
		
			polygon_list.append(a)
			

		zero_mask = np.zeros([self.shapes[1], self.shapes[0]], np.uint8)
			
		polyMask = cv2.fillPoly(zero_mask, polygon_list[0], 1)
			
		fname = self.file_name + ".png"
		
		polyRange = [x for x in range(1, num_shapes)]
		
		for q in polyRange:
			x = q+1
			polyMask = cv2.fillPoly(polyMask, polygon_list[q], x)
			
		cv2.imwrite(fname, polyMask)
				
		return print("File " + self.file_name + ".png created successfully")
			
		
#json2png = Mask(annotation_file, images_dir, output_filename)

