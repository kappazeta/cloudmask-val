import argparse
from matplotlib import pyplot as plt
import cv2 as cv
import mpldatacursor
import numpy as np
import matplotlib.patches as patches

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="path to input image")
parser.add_argument("--ratio", required=True, help="rescaling ratio (eg 0.2 - 20% of original resolution)")
parser.add_argument("--label", default=False, choices=["True", "False"], help="use this if you want to see information about label image or prediction image")

a = parser.parse_args()

#Read in and resize the image

img=cv.imread(a.input)
height, width, channels = img.shape
ratio=float(a.ratio)
img=cv.resize(img,dsize=(int(height*ratio),int(width*ratio)))

#Open the image interactively in matplotlib

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(img)

#Create a rectangle to show the border of individual tile

rect = patches.Rectangle((1000,1000),512*ratio,512*ratio,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)

color_to_label = {
    tuple([255, 255,255]): "True cloud",
    tuple([0, 0,0]): "True clear",
    tuple([190, 190, 190]): "True cloudshadow",
    tuple([100,100,100]): "True semitransparent",
    
    tuple([0,255,255]): " Cloud instead of clear",
    tuple([0,0,255]): " Cloud instead of cloud shadow",
    tuple([135,206,235]): "Cloud instead of semitransparent cloud",
    
    tuple([0,255,0]): "Clear instead of cloud",
    tuple([240,230,140]): "Clear instead of cloudshadow",
    tuple([60,179,113]): "Clear instead of semitransparent",
    
    tuple([255, 201, 0]): "Shadow instead of cloud",
    tuple([255,255,0]): "Shadow instead of clear",
    tuple([204,204,0]): "Shadow instead of semitransparent",
    
    tuple([240,128,128]): "Semitransparent instead of cloud",
    tuple([255,0,0]): "Semitransparent instead of clear",
    tuple([220,20,60]): "Semitransparent instead of shadow",
    
    tuple([255,0,255]): "True undefined",
    tuple([238,130,238]): "Undefined predicted instead of sth else",
    tuple([153,50,204]): "Predicted something else instead of undefined"
    }

if(a.label):
    color_to_label = {
        tuple([3,3,3]): "Undefined",
        tuple([66,66,66]): "Clear",
        tuple([129,129,129]): "Cloud shadow",
        tuple([192,192,192]): "Semitransparent cloud",
        tuple([255,255,255]): "Cloud",  
    }

#All the possible coordinates of individual tiles

vertical_lines_locations=np.arange(512*ratio/2,ratio*width,512*ratio)
horizontal_lines_locations=np.arange(512*ratio/2,ratio*height,512*ratio)

#Draw rectangle according to cursor position    

def on_mouse_move(event):
    if None not in (event.xdata, event.ydata):
        x=int(min(vertical_lines_locations, key=lambda x:abs(x-event.xdata))-512*ratio/2)    #This picks the right coordinate for the rectangle
        y=int(min(horizontal_lines_locations, key=lambda x:abs(x-event.ydata))-512*ratio/2)
        rect.set_xy((x,y))
        fig.canvas.draw()

fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

#Display the label and tile info as the cursor moves

def myformatter(**kwarg):
    label = '{x:.0f},{y:.0f}'.format(**kwarg)
    i=int(label.split(",")[0]) #x-koord
    j=int(label.split(",")[1]) #y-koord
    RGB=tuple(img[j, i])
    label=color_to_label.get(RGB)
    tile_x=int(i*(1/ratio)/512)
    tile_y=int(j*(1/ratio)/512)
    label="tile_"+str(tile_x)+"_"+str(tile_y)+"\n"+str(label)
    return label

mpldatacursor.datacursor(hover=True, bbox=dict(alpha=1, fc='w'),formatter=myformatter)
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
ax.axis('off')
plt.show()

