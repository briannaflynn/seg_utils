import cv2 as cv
import numpy as np
import pandas as pd
from torch import IntTensor
import torch.nn as nn
from PIL import Image
import sys

path_to_files = sys.argv[1]
filenames = path_to_files + "color.txt"
out_dir = sys.argv[2]

with open(filenames, "r") as fd:
	lines = fd.read().splitlines()
	
def png2color(file, *colors):
  img = Image.open(file)
  data = np.asarray(img)
  d = np.copy(data)

  num_poly = len(np.unique(d)) - 1
  assert num_poly == len(colors), "Number of colors provided must match number of polygons in image"
  for i in range(num_poly):
    d[d == (i + 1)] = colors[i]

  cv.imwrite("./" + file[:-4] + "_colored.png", )

  return np.unique(d)
  
png2color(lines, 80, 140, 220)