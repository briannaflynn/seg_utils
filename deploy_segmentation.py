from fastai.vision import *
from fastai.callbacks.hooks import *
from fastai.utils.mem import *
import os
from shutil import copyfile
import cv2 as cv
import pandas as pd
from torch import IntTensor
import torch.nn as nn
from PIL import Image
import sys
import time

def timeit(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        retval = func(*args, **kwargs)
        print('{} took {:.5f}s'.format(func.__name__, time.time() - now))
        return retval
    return wrapper
# GLOBAL: METRICS USED WHILE TRAINING
# These must be global or else this breaks, just for segmentation
def acc(input, target):
    target = target.squeeze(1)
    
    return (input.argmax(dim=1)==target).float().mean()

metrics=acc

def loadLearner(path_to_pkl, pkl):
	
	wd = 1e-2
	
	learn = load_learner(path_to_pkl, pkl)
	
	return learn

# path to images, deploy.txt and .pkl file

path = sys.argv[1]
fname = path + "deploy.txt"

with open(fname, "r") as fd:
	lines = fd.read().splitlines()
	
# path to the destination directory
out = sys.argv[2]
# name of the learner.pkl file
learner = sys.argv[3]

# get the learner object
pickl = loadLearner(path, learner)

@timeit
def segrunner(files:list, path:str, pkl, out_dir:str):

	def pred2png(pred, input, out_dir):
		input = os.path.basename(input)
		out_file = input[:-4] + "_prediction.png"
		out_file = out_dir + out_file
		
		x = pred[1]
		j = x.numpy()
		j_int = j.astype(np.int)
		
		j = np.squeeze(j_int)
		print("... Attempting to write", out_file)
		cv.imwrite(out_file, j)
		print(out_file, "successfully written")
		
	for f in files:
		
		filepath = path + f
		img = open_image(filepath)
		pred = pkl.predict(img)
		pred2png(pred, filepath, out_dir)
		
		
segrunner(lines, path, pickl, out)