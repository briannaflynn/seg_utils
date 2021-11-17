import cv2 as cv
import numpy as np
import pandas as pd
from torch import IntTensor
import torch.nn as nn
from PIL import Image
import sys

# GLOBAL INPUTS
path_to_files = sys.argv[1]
filenames = path_to_files + "color.txt"
out_dir = sys.argv[2]

# READ FILENAMES IN COLOR.TXT AS LIST
with open(filenames, "r") as fd:
	lines = fd.read().splitlines()

# FUNCTION THAT CONVERTS PNG TO NEW NP ARRAY, REPLACES SEQUENTIAL POLYGON NUMS WITH GRAYSCALE COLOR VALS, WRITES COLORED IMAGE TO OUT DIRECTORY	
def png2color(f, *colors):
	
	file = path_to_files + f
	img = Image.open(file)
	data = np.asarray(img)
	d = np.copy(data)
	
	num_poly = len(np.unique(d)) - 1
	assert num_poly == len(colors), "Number of colors provided must match number of polygons in image"
	for i in range(num_poly):
		d[d == (i + 1)] = colors[i]
		
	cv.imwrite(out_dir + f[:-4] + "_colored.png", d)

# FOR ALL FILES IN COLOR.TXT MAKE COLORED PNG USING THESE THREE COLORS: 80, 140, 220 (larger is whiter, smaller is darker gray)	
for l in lines:
	png2color(l, 80, 140, 220)