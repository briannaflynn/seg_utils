#!/usr/bin/python

from metrics import *
from skimage.io import imread
import os
from os import listdir
import pandas as pd
import argparse

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Convert JSON annotation to mask PNG image")
	parser.add_argument('--y_true', action='store', type=str, required = True, help ='Path to ground truth image')
	parser.add_argument('--y_pred', action='store', type=str, required = True, help='Path to prediction image')

	args = parser.parse_args()
  y_true = args.y_true
  y_pred = args.y_pred
  
  y_true = imread(y_true)
	y_pred = imread(y_pred)
		
	p_a = pixel_accuracy(y_pred, y_true)
	m_i = mean_IU(y_pred, y_true)
  
  mean_iou = m_i[0]
  polygon_ious = m_i[1]
  
  metrics = {"Filename": y_true, "Pixel Accuracy": p_a, "Mean IOU": mean_iou, "Individual Polygon IOUs": polygon_ious}
  print(metrics)
