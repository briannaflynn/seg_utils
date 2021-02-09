#!/usr/bin/python

from json2mask import Mask
import os
			
jsons = os.listdir('/full/file/path/to/JSON/')
#print(jsons) This contains a list of all files in a directory (ideally containing all JSON annotation files)

for j in jsons:
	json2png = Mask('/full/file/path/to/JSON/' + j, '/full/file/path/to/all_images', j + '_mask')
	json2png.drawMask()
