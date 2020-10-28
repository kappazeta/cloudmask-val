import sys
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
from matplotlib import cm

input_folder=sys.argv[1]
label=sys.argv[2]

#0 - undefined
#64 - clear
#127 - cloud shadow
#191 - semitransparent cloud
#255 - cloud

#Mask values:
#3 - undefined
#66 - clear
#129 - cloud shadow
#192 - semitransparent
#255 - cloud

prediction=input_folder+'/prediction.png'
real_mask=input_folder+'/label.png'

with Image.open(prediction) as im:
    p = np.array(im, dtype=np.float)
    pix = np.array(im, dtype=np.float)
    
with Image.open(real_mask) as im:
    m = np.array(im, dtype=np.float)
    
if(label=="cloud"):
    p_val=255
if(label=="clear"):
    p_val=66
if(label=="cloudshadow"):
    p_val=129
if(label=="semitransparent"):
    p_val=192
if(label=="undefined"):
    p_val=3

truepositive = ((p==p_val) & (m==p_val))
falsepositive = ((p==p_val) & (m!=p_val))
truenegative = ((p!=p_val) & (m!=p_val))
falsenegative = ((p!=p_val) & (m==p_val))

#Now actually assing labels (1-4) to masks and map them to some color

pix=np.where(truepositive==False, pix, 1)
pix=np.where(truenegative==False, pix, 2)
pix=np.where(falsepositive==False, pix, 3)
pix=np.where(falsenegative==False, pix, 4)


label_to_color = {
    1: [255,255,255], # True positive: white
    2: [0,0,0], #True negative: black
    3: [170,170,170], #False positive: lighter grey
    4: [85,85,85] #False negative: darker grey
    }
    
#Create the rgb-image

rgb_img = np.zeros((*pix.shape, 3))
 
for key in label_to_color.keys():
    rgb_img[pix == key] = label_to_color[key]

im_result = Image.fromarray(np.uint8(rgb_img))

#In order to include the legend, open this image in matplotlib

gs = GridSpec(6,1)

fig = plt.figure(figsize = (10,10))
ax1 = fig.add_subplot(gs[:-1,:]) ##for the plot
ax2 = fig.add_subplot(gs[-1,:])   ##for the legend

ax1.imshow(im_result)

legend_data=[[1,[255, 255,255],"True positive"],[2,[0,0,0],"True negative"],[3,[190, 190, 190],"False positive"],[4,[100,100,100],"False negative"]]

handles = [Rectangle((0,0),1,1, color = tuple((v/255 for v in c))) for k,c,n in legend_data]
labels = [n for k,c,n in legend_data]

ax2.legend(handles,labels, mode='expand', ncol=2)

ax2.axis('off')
ax1.axis('off')

plt.savefig(input_folder+"/"+label+"_confusion_info.png" ,bbox_inches = 'tight',pad_inches = 0)
        
