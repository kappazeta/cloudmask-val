import sys
import os
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
from matplotlib import cm

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="path to prediction folder of experiment")
a = parser.parse_args()
input_folder=a.input

predict=input_folder+'/prediction.png'
mask=input_folder+'/label.png'
s2cmask=input_folder+'/SCL.png'

with Image.open(mask) as im:
    m = np.array(im, dtype=np.float)
    pix = np.array(im, dtype=np.float)
    
with Image.open(predict) as im:
    p = np.array(im, dtype=np.float)
    
with Image.open(s2cmask) as im:
    s2c = np.array(im, dtype=np.float)
    
#Pixel values:
#3 - undefined
#66 - clear
#129 - cloud shadow
#192 - semitransparent
#255 - cloud

#Create masks:

#both true

p_cloud_s_cloud_true=((p==255) & (s2c==255) & (m==255))
p_clear_s_clear_true=((p==66) & (s2c==66) & (m==66))
p_shadow_s_shadow_true=((p==129) & (s2c==129) & (m==129))
p_semi_s_semi_true=((p==192) & (s2c==192) & (m==192))
p_undef_s_sundef_true=((p==3) & (s2c==3) & (m==3))

#both false

both_false=((p!=m) & (s2c!=m))

#Prediction 2, se2cor false

p_true_s_false = ((p==m) & (s2c != m))

#s2cor true, prediction false

p_false_s_true = ((p!=m) & (s2c == m))


'''
existing_labels=[]

#Return False if all elements are False

def check(mask): 
    result = False;
    if(len(mask) > 0 ):
        result = all(all(elem == False) for elem in mask)
    return result

if(check(true_cloud)==False):
    existing_labels.append(1)
if(check(true_clear)==False):
    existing_labels.append(2)
if(check(true_cloudshadow)==False):
    existing_labels.append(3)
if(check(true_semitransparent)==False):
    existing_labels.append(4)
if(check(predictedcloud_instead_clear)==False):
    existing_labels.append(5)
if(check(predictedcloud_instead_cloudshadow)==False):
    existing_labels.append(6)
if(check(predictedcloud_instead_semitransparent)==False):
    existing_labels.append(7)
if(check(predictedclear_instead_cloud)==False):
    existing_labels.append(8)
if(check(predictedclear_instead_cloudshadow)==False):
    existing_labels.append(9)
if(check(predictedclear_instead_semitransparent)==False):
    existing_labels.append(10)
if(check(predictedshadow_instead_cloud)==False):
    existing_labels.append(11)
if(check(predictedshadow_instead_clear)==False):
    existing_labels.append(12)
if(check(predictedshadow_instead_semitransparent)==False):
    existing_labels.append(13)
if(check(predictedsemitransparent_instead_cloud)==False):
    existing_labels.append(14)
if(check(predictedsemitransparent_instead_clear)==False):
    existing_labels.append(15)
if(check(predictedsemitransparent_instead_cloudshadow)==False):
    existing_labels.append(16)
if(check(true_undefined)==False):
    existing_labels.append(17)
if(check(predictedundefined_instead_)==False):
    existing_labels.append(18)
if(check(predicted_instead_undefined)==False):
    existing_labels.append(19)

'''
#Now actually assing labels (1-16) to masks and map them to some color

pix=np.where(p_cloud_s_cloud_true==False, pix, 1)
pix=np.where(p_clear_s_clear_true==False, pix, 2)
pix=np.where(p_shadow_s_shadow_true==False, pix, 3)
pix=np.where(p_undef_s_sundef_true==False, pix, 4)
pix=np.where(p_semi_s_semi_true==False, pix, 5)
pix=np.where(both_false==False, pix, 6)
pix=np.where(p_true_s_false==False, pix, 7)
pix=np.where(p_false_s_true==False, pix, 8)


label_to_color = {
    1: [255, 255,255], # True cloud: white
    2: [66, 66,66], #True clear: black
    3: [129, 129, 129], #True cloudshadow: lighter grey
    4: [3,3,3], #True undefined
    5: [192,192,192], # True semitransparent
    6: [153,50,204], # Both false
    7: [0,255,0], # Prediction true, sen2cor false
    8: [255,0,0], #S2cor true, prediction false
    }
    
#Create the rgb-image

rgb_img = np.zeros((*pix.shape, 3))
 
for key in label_to_color.keys():
    rgb_img[pix == key] = label_to_color[key]

im_result = Image.fromarray(np.uint8(rgb_img))

im_result.save(input_folder+"/s2c_comparison.png")

'''
#In order to include the legend, open this image in matplotlib

gs = GridSpec(6,1)

fig = plt.figure(figsize = (10,12))
ax1 = fig.add_subplot(gs[:-1,:]) ##for the plot
ax2 = fig.add_subplot(gs[-1,:])   ##for the legend

ax1.imshow(im_result)

legend_labels=["True cloud","True clear","True cloudshadow","True undefined","True semitransparent","Both models false","Pred. true, s2c false","S2c true, pred. false"]

legend_data=[]

existing_labels=np.arange(1,9,1)

for nr in existing_labels:
    temp=[]
    temp.append(nr)
    temp.append(label_to_color[nr])
    temp.append(legend_labels[nr-1])
    legend_data.append(temp)

handles = [Rectangle((0,0),1,1, color = tuple((v/255 for v in c))) for k,c,n in legend_data]
labels = [n for k,c,n in legend_data]

ax2.legend(handles,labels, mode='expand', ncol=3)
ax2.axis('off')
ax1.axis('off')

plt.savefig(input_folder+"/s2c_comparison.png" ,bbox_inches = 'tight',pad_inches = 0)
'''       
