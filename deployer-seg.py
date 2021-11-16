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

# path to directory with deploy.txt and images
p = sys.argv[1]
# name of the output csv file
name = sys.argv[2]
# model
model = sys.argv[3]
# path to model
q = sys.argv[4]

fname = p + "/deploy.txt"

with open(fname, "r") as fd:
    lines = fd.read().splitlines()

def acc(input, target):
    target = target.squeeze(1)
    
    return (input.argmax(dim=1)==target).float().mean()

metrics=acc

def loadLearner(path_to_pkl):
    
    wd=1e-2 # weight decay
    
    learn = load_learner(path_to_pkl)
    
    return learn

def pred2png(pred, in_file, out_dir = "./"):
    
    input = os.path.basename(in_file)
    out_file = input[:-4] + "_prediction.png"
    out_file = out_dir + out_file
    
    image = Image.open(in_file)
    shape = image.size
    
    x = pred[1]

    j = x.numpy()
    j_int = j.astype(np.int)
    
    j = np.squeeze(j_int)
    # j is the matrix containing the numbers, np.unique j is the number of polygons annotated in each image
    # print(j, np.unique(j))
    cv.imwrite(out_file, j)
    
    print(out_file) 

def runner(files, path, out_dir = "./"):
	
	p = None
	if path[-1] == "/":
		p = path
	else:
		p = path + "/"
		
	for f in files:
		input = p + f
		img = open_image(input)
		pred = learn.predict(img)
		
		pred2png(pred, input, out_dir)
		
		
		
class deploy:

	def __init__(self, p, name, q, model):
		self.path = p
		self.out_name = name
		self.model_path = q
		self.model_name = model
		
		fname = p + "/deploy.txt"
		
		with open(fname, "r") as fd:
			lines = fd.read().splitlines()
		self.files = lines 
		
		def data_init(cols):
			df = pd.DataFrame()
			for i in range(len(cols)):
				c = cols[i]
				df[c] = None
			return df
			
		self.df = data_init(['file', 'prediction', 'probability'])
		
	def segLearner(path_to_pkl, wd = 1e-2):
		
		wd = wd
		
		learn = load_learner(path_to_pkl)
		
		return learn
		
	def classLearner(path_to_pkl, model):
	
		learn = load_learner(path_to_pkl, model)
		
		return learn
		
	
		
	
		
		