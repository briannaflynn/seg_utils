#!/usr/bin/python

from json2mask import Mask
import os
			
def json_Iterator(annotation_dir_path:str, image_dir_path:str):
	jsons = os.listdir(annotation_dir_path)
	
	for j in jsons:
		json2png = Mask(annotation_dir_path + j, image_dir_path, j + '_mask')
		json2png.drawMask()
		
if __name__ == "__main__":
	
	JSON_path = "./JSON_annotations"
	image_path = "./all_images"
	
	json_Iterator(JSON_path, image_path)
	
'''
Double and triple check the dimensions of the mask files! issues with memory can cause the masks to be offset in height and will cause problems during training (always check training data as well to make sure there's no dimension matching issues)
'''
