#!/usr/bin/python

# TODO: ADD OPTIONAL ARGS FOR OTHER IMAGES

from metrics import *
from skimage.io import imread
import os
from os import listdir
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Interpret predictions using pixel accuracy, mean IOU, and per polygon IOU")
parser.add_argument('--polygon', action='store', type=str, default=None, help= 'Provide polygon list for ious, current option is: spine')
parser.add_argument('--dir_y_true', action = 'store', type = str, required = True, help = 'Directory with ground truth images')
parser.add_argument('--dir_y_pred', action = 'store', type = str, required = True, help = 'Directory with predictions') 
parser.add_argument('--df_name', action = 'store', type = str, default = None, help = 'Create a dataframe with results')

args = parser.parse_args()

poly = args.polygon
true_dir = args.dir_y_true
pred_dir = args.dir_y_pred
df_name = args.df_name

metric_list = []

if true_dir and pred_dir != None:
	truths = os.listdir(true_dir)
	preds = os.listdir(pred_dir)
	
	a = None
	j = None
	
	
	for i in range(len(truths)):
		if truths[i] == preds[i]:
			a, j = truths[i], preds[i]
			
			tr = true_dir + '/' + a
			pr = pred_dir + '/' + j
			
			y_true = imread(tr)
			y_pred = imread(pr)
			
			p_a = pixel_accuracy(y_pred, y_true)
			m_i = mean_IU(y_pred, y_true)
			
			mean_iou = m_i[0]
			polygon_ious = m_i[1]
			lmean = np.mean(polygon_ious[1:5])
			if poly == "spine":
				polygons = ["T12", "L1", "L2", "L3", "L4", "L5"]
				polydict = dict(zip(polygons, polygon_ious))
				metrics = {"Filename": pr, "Pixel Accuracy": p_a, "Mean IOU": mean_iou, "Individual Polygon IOUs": polydict, "L1-L4 Mean IOU": lmean}
				metric_list.append(metrics)
			
			elif poly == None:
				metrics = {"Filename": pr, "Pixel Accuracy": p_a, "Mean IOU": mean_iou, "Individual Polygon IOUs": polygon_ious, "L1-L4 Mean IOU": lmean}
				metric_list.append(metrics)


a = [{**x, **x.pop('Individual Polygon IOUs')} for x in metric_list]

if df_name != None:
	df = pd.DataFrame(a)
	df.to_csv(df_name, index=False)
	


