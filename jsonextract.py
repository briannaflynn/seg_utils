#!/usr/bin/env python
import json 
import os
from PIL import Image
import cv2
import numpy as np
from os import listdir
import argparse

# Main Functions
# Get coordinates from json
# get a mask from a coordinate dictionary

def coordinates_from_json(filename, json_path):
    file = open(json_path)
    data = json.load(file)
    file.close() #we now have the json object as a python dictionary
    d = data[filename]['regions']
    poly_length = len(list(d.values()))
    xcoords = []
    ycoords = []
    keys = []
    for i in range(poly_length):
    	i = str(i)
    	x = data[filename]['regions'][i]['shape_attributes']['all_points_x']
    	y = data[filename]['regions'][i]['shape_attributes']['all_points_y']
    	k = data[filename]['regions'][i]['region_attributes']['label']
    	xcoords.append(x)
    	ycoords.append(y)
    	keys.append(k)
    	
    cdict = {}
    cdict['img_name'] = filename
    
    
    for i in range(poly_length):
    	cdict[keys[i]] = {'x': xcoords[i], 'y': ycoords[i]}
    
    return cdict
        
def mask_from_dict(coords_dict, img_dir, dest_dir, color = False):
	filename = coords_dict['img_name']
	path = os.path.abspath(img_dir + '/' + filename)
	image = Image.open(path)
	shape = image.size
	image.close()
	
	zero_mask = np.zeros([shape[1], shape[0]], np.uint8)
		
	polygon_list = []
	
	k = list(coords_dict.keys())
	keys = k[1:]
	
	for b in keys:
		contours = np.stack((coords_dict[b]['x'], coords_dict[b]['y']), axis = 1)
		c = np.array([contours], dtype = np.int32)
		polygon_list.append(c)
	
	num_shapes = len(keys)
	polyRange = [x for x in range(1, num_shapes)]
	
	if color == True:
		x = 60
		polyMask = cv2.fillPoly(zero_mask, polygon_list[0], x)
		for q in polyRange:
			x += 30
			polyMask = cv2.fillPoly(polyMask, polygon_list[q], x)
	
	if color == False:
		x = 1
		polyMask = cv2.fillPoly(zero_mask, polygon_list[0], x)
		for q in polyRange:
			x += 1
			polyMask = cv2.fillPoly(polyMask, polygon_list[q], x)
		
	fname = filename[:-4] + ".png"
	
	fname = dest_dir + "/" + fname
	cv2.imwrite(fname, polyMask)
	return print("File " + fname + " created successfully")

# CLI for getting json, image dir, and destination directory. Optional arg to color the resulting mask for inspection
if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Convert JSON annotation to mask PNG image")
	parser.add_argument('--json_path', action='store', type=str, required = True, help ='Path to JSON annotations (in VGG format using makesense.ai annotation tool)')
	parser.add_argument('--input_dir', action='store', type=str, required = True, help='Directory with the raw JPG images that were annotated')
	parser.add_argument('--dest_dir', action='store', type=str, required = True, help='Directory with the resulting mask png files')
	parser.add_argument('--color', action = 'store', type=bool, default = False, help = 'Option for coloring annotations. Set --color True if you want to color the output for a quick visual check (the default is False, the format needed for downstream processes)')

	args = parser.parse_args()
	json_path = args.json_path
	input_dir = args.input_dir
	dest_dir = args.dest_dir
	color_status = args.color
	
	file = open(json_path)
	data = json.load(file)
	files = [j for j in data.keys()]
	
	coords = []
	for f in files:
		try:
			coords.append(coordinates_from_json(f, json_path))
		except FileNotFoundError:
			print("File " + f + " not found")
	
	for c in coords:
		mask_from_dict(c, input_dir, dest_dir, color_status)
	