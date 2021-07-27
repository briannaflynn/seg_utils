#!/usr/bin/python

import pydicom as dicom
import pandas as pd
import os
import glob
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import pickle
from PIL import Image
from skimage.io import imread
import argparse

def add_pad(image, new_height, new_width):
    height, width = image.shape

    final_image = np.zeros((new_height, new_width))

    pad_left = int((new_width - width) / 2)
    pad_top = int((new_height - height) / 2)
    
    final_image[pad_top:pad_top + height, pad_left:pad_left + width] = image
    
    return final_image
    	
def dicom_to_padded_image(dicom_dir, row_val:tuple, col_val:tuple, height_pad, width_pad, out_dir, img_type = ".jpg"):
	
	def ext_only(directory, extension='dcm'):
		return([f for f in os.listdir(directory) if f.endswith('.' + extension)])
	
	for file in ext_only(dicom_dir):
		img = os.path.join(dicom_dir, file)
		outimg = os.path.join(out_dir, file)
		sample = dicom.dcmread(img)
		image = sample.pixel_array
		
		rows = sample[0x00280010].value
		cols = sample[0x00280010].value
		
		if rows >= row_val[0] and rows <= row_val[1] and cols >= col_val[0] and cols <= col_val[1]:
			padded_image = add_pad(image, height_pad, width_pad)
			padded_string = "_padded" + img_type
			outimg = outimg.replace('.dcm', padded_string)
			cv2.imwrite(outimg, padded_image)
			print(outimg, "written!")
		else:
			print('size requirement not met')
			
		return None

def annotation_to_padded_image(annotation_dir, row_val:tuple, col_val:tuple, height_pad, width_pad, out_dir):
	
	def ext_only(directory, extension='png'):
		return([f for f in os.listdir(directory) if f.endswith('.' + extension)])
	
	for file in ext_only(annotation_dir):
		img = os.path.join(annotation_dir, file)
		image = Image.open(os.path.join(annotation_dir, file))
		outimg = os.path.join(out_dir, file)
		shape = image.size
		image.close()
		
		im = imread(img)
		cols = shape[0]
		rows = shape[1]
		
		if rows >= row_val[0] and rows <= row_val[1] and cols >= col_val[0] and cols <= col_val[1]:
			padded_image = add_pad(im, height_pad, width_pad)
			padded_string = "_padded.png"
			outimg = outimg.replace('.dcm', padded_string)
			cv2.imwrite(outimg, padded_image)
			print(outimg, "written!")
		else:
			print('size requirement not met')
		
		return None

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Convert images to padded images")
	
	parser.add_argument('--dicom_directory', action='store', type=str, required = True, help ='Path to DICOM image directory')
	parser.add_argument('--annotation_directory', action='store', type=str, default = None, help ='Path to annotation image directory')
	parser.add_argument('--jpg_output_directory', action ='store', type = str, required = True, help = 'Path to output directory for padded JPG images')
	parser.add_argument('--annotation_output_directory', action = 'store', type = str, default = None, help = 'Path to padded annotation directory')
	parser.add_argument('--row_values', action = 'store', nargs = '+', required = True, help = 'Tuple containing range for row value')
	parser.add_argument('--column_values', action = 'store', nargs = '+', required = True, help = 'Tuple containing range for column values')
	parser.add_argument('--padded_height', action = 'store', type = int, required = True, help = 'Height of padded image')
	parser.add_argument('--padded_width', action='store', type = int, required = True, help = "Width of padded image")
	
	args = parser.parse_args()
	dcm = args.dicom_directory
	annots = args.annotation_directory
	jpg_out = args.jpg_output_directory
	annots_out = args.annotation_output_directory
	rows = tuple([int(f) for f in args.row_values])
	cols = tuple([int(f) for f in args.column_values])
	print(rows, cols)
	height = args.padded_height
	width = args.padded_width
	
	print(height, width)
	
	dicom_to_padded_image(dcm, rows, cols, height, width, jpg_out, img_type = ".jpg")
	
	if annots and annots_out != None:
		annotation_to_padded_image(annots, rows, cols, height, width, annots_out)

