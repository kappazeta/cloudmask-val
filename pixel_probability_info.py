import argparse
from matplotlib import pyplot as plt
import cv2 as cv
import mpldatacursor
import numpy as np
import matplotlib.patches as patches
import tkinter as tk
from tkinter import messagebox
import os.path 
import matplotlib

matplotlib.use('TkAgg')

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="path to input folder")


a = parser.parse_args()

undefined=cv.imread(a.input+"predict_UNDEFINED.png")
clear=cv.imread(a.input+"predict_CLEAR.png")
shadow=cv.imread(a.input+"predict_CLOUD_SHADOW.png")
semi=cv.imread(a.input+"predict_SEMI_TRANSPARENT_CLOUD.png")
cloud=cv.imread(a.input+"predict_CLOUD.png")

original=a.input+"prediction.png"

img=cv.imread(original)

#Open the image interactively in matplotlib

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(img)

#Display the label and tile info as the cursor moves

def myformatter(**kwarg):
    label = '{x:.0f},{y:.0f}'.format(**kwarg)
    j=int(label.split(",")[0]) #x-koord
    i=int(label.split(",")[1]) #y-koord

    cloud_prob=float(cloud[i][j][0]/255*100)
    clear_prob=float(clear[i][j][0]/255*100)
    shadow_prob=float(shadow[i][j][0]/255*100)
    semi_prob=float(semi[i][j][0]/255*100)
    undefined_prob=float(undefined[i][j][0]/255*100)

    label="Cloud probability: "+"{:.4f}".format(cloud_prob)+"%\nClear probability: "+"{:.4f}".format(clear_prob)+"%\nShadow probability: "+"{:.4f}".format(shadow_prob)+"%\nSemitransparent probability: "+"{:.4f}".format(semi_prob)+"%\nUndefined probability: "+"{:.4f}".format(undefined_prob)+"%"
    return label

mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'),formatter=myformatter)
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
ax.axis('off')
plt.show()


