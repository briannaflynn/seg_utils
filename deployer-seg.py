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
import datetime


# GLOBAL: METRICS USED WHILE TRAINING
# These must be global or else this breaks, just for segmentation
def acc(input, target):
    target = target.squeeze(1)
    
    return (input.argmax(dim=1)==target).float().mean()

metrics=acc

# INPUT: Necessary for both classification and segmentation

# path to directory with deploy.txt, images and pkl file
p = sys.argv[1]
# name of pkl file
pkl = sys.argv[2]
# path to model
q = sys.argv[3]
# model
model = sys.argv[4]
# What type of model are you deploying? OPTIONS: SEGMENTATION OR CLASSIFICATION
type = None
if sys.argv[5] == "segmentation":
	type = True
	
elif sys.argv[5] == "classification":
	type = False
		
print(type)	

#get current date and time
x = datetime.datetime.now()
#convert date and time to string
dateTimeStr = str(x)
#print the date and time string
print(dateTimeStr)

name = "classification_" + dateTimeStr + ".csv"
print(name)
################################################################################

# Class Deploy
# Funcs: Get predictions from trained segmentation and classification models
		
class deploy:

	def __init__(self, p, name, q, model, type):

		self.path = p
		self.out_name = name
		self.model_path = q
		self.model_name = model
		self.type = type
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
			
	def pred2png(pred, input, out_dir = "./"):
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
		
	
	def segLearner(path_to_pkl, model):
		
		wd = 1e-2
		learn = load_learner(path_to_pkl, model)
		
		return learn
		
	def segDeploy(img, learner, input, out):
	
		pred = learner.predict(img)
		j = pred2png(pred, input, out)
		
		return j
		
		
	def classLearner(path_to_pkl, model):
	
		learn = load_learner(path_to_pkl, model)
		
		return learn
		
	def classDeploy(img, learner, df):
		
		pred = learner.predict(img)
		pr = IntTensor.item(pred[1])
		prob = pred[2].numpy()
		
		j = {'file':f, 'prediction':pr, 'probability':prob}
		df = df.append(j, True)
		
		return df
		
	def runner(files, path, learner, out_dir = None, segment = True, df = None):
	
		def pred2png(pred, in, out_dir = "./"):
			input = os.path.basename(input)
			out_file = input[:-4] + "_prediction.png"
			out_file = out_dir + out_file
			
			x = pred[1]
			j = x.numpy()
			j_int = j.astype(np.int)
			
			j = np.squeeze(j_int)
			print("...Attempting to write", out_file)
			cv.imwrite(out_file, j)
			print(out_file, "successfully written")
			
		p = None
		if path[-1] == "/":
			p = path
		else:
			p = path + "/"
		
		# Method 1: iterate through files first, then triage based on type
# 		for f in files:
# 			input = p + f
# 			img = open_image(input)
# 			
# 			if segment == True:
# 				
# 				segDeploy(img, learner, input, out_dir)
# 				# pred = learner.predict(img)
# 				pred2png(pred, input, out_dir)
# 				
# 			else:
# 			
# 				classDeploy(img, learner, df)
			
				# pred = learner.predict(img)
# 				pr = IntTensor.item(pred[1])
# 				prob = pred[2].numpy()
# 				
# 				j = {'file':f, 'prediction':pr, 'probability':prob}
# 				df = df.append(j, True)
		
		# Method 2: Triage by type first, then iterate through files		
		def iterfil(p,f):
		
			input = p+f
			img = open_image(input)
			return img
		
		if segment == True:
			print("... Deploying segmentation model")
		
			for f in files:
			
				img = iterfil(p, f)
				in = p + f
				#segDeploy(img, learner, out_dir)
				
				pred = learner.predict(img)
				pred2png(pred, in, out_dir)
				
		else:
			
			for f in files:
				
				img = iterfil(p, f)
				
				pred = learner.predict(img)
				pr = IntTensor(item(pred[1]))
				prob = pred[2].numpy()
				
				j = {'file':f, 'prediction':pr, 'probability':prob}
				df = df.append(j, True)
			
			return df


################################################################################

# TEST: Segmentation

d = deploy(p, name, q, model, type)
lines = d.files
print(lines)
learner = deploy.segLearner('/scratch1/05515/bflynn/knee/right_knee/padded_right_knee/', 'knee_segmentation.pkl')
p = '/scratch1/05515/bflynn/knee/right_knee/padded_right_knee/'
deploy.runner(lines,  p, learner, "./", segment = type)
# 
