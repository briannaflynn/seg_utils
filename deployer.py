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

learn = load_learner(q, model)

def data_init(cols):
    
    df = pd.DataFrame()
    for i in range(len(cols)):
        c = cols[i]
        df[c] = None
        
    return df
    
df = data_init(['file', 'prediction', 'probability'])

def runner(files, path, df):
    
    for f in files:
        input = path + "/" + f
        img = open_image(input)
        
        pred = learn.predict(img)
        pr = IntTensor.item(pred[1])
        prob = pred[2].numpy()
        
        j = {'file':f, 'prediction': pr, 'probability':prob}
        df = df.append(j, True)
        
    return df
    
data = runner(lines, p, df)
data.to_csv(name, index=False)
