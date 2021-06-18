#!/usr/bin/python

# TODO: ADD OPTIONAL ARGS FOR OTHER IMAGES

from metrics import *
from skimage.io import imread
import os
from os import listdir
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Interpret predictions using pixel accuracy, mean IOU, and per polygon IOU")
parser.add_argument('--y_true', action='store', type=str, required = True, help ='Path to ground truth image')
parser.add_argument('--y_pred', action='store', type=str, required = True, help='Path to prediction image')
parser.add_argument('--polygon', action='store', type=str, default=None, help= 'Provide polygon list for ious, current option is: spine') 

args = parser.parse_args()
y_true_name = args.y_true
y_pred_name = args.y_pred
poly = args.polygon

y_true = imread(y_true_name)
y_pred = imread(y_pred_name)

p_a = pixel_accuracy(y_pred, y_true)
m_i = mean_IU(y_pred, y_true)

mean_iou = m_i[0]
polygon_ious = m_i[1]

if poly == "spine":
	polygons = ["T12", "L1", "L2", "L3", "L4", "L5"]
	polydict = dict(zip(polygons, polygon_ious))
	metrics = {"Filename": y_pred_name, "Pixel Accuracy": p_a, "Mean IOU": mean_iou, "Individual Polygon IOUs": polydict}
	print(metrics)

elif poly == None:
	metrics = {"Filename": y_pred_name, "Pixel Accuracy": p_a, "Mean IOU": mean_iou, "Individual Polygon IOUs": polygon_ious}
	print(metrics)
