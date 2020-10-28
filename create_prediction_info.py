import sys
import os
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
from matplotlib import cm

input_folder=sys.argv[1]
tiles_with_undefined=sys.argv[2]

predict=input_folder+'/prediction.png'
mask=input_folder+'/label.png'

with Image.open(mask) as im:
    m = np.array(im, dtype=np.float)
    pix = np.array(im, dtype=np.float)
    
with Image.open(predict) as im:
    p = np.array(im, dtype=np.float)
    
#Pixel values:
#3 - undefined
#66 - clear
#129 - cloud shadow
#192 - semitransparent
#255 - cloud

#Create masks:
    
true_cloud=((m==255) & (p==255))
true_clear=((m==66) & (p==66))
true_cloudshadow=((m==129) & (p==129))
true_semitransparent=((m==192) & (p==192))
true_undefined=((m==3) & (p==3))

predictedcloud_instead_clear = ((p==255) & (m==66))
predictedcloud_instead_cloudshadow=((p==255) & (m==129))
predictedcloud_instead_semitransparent=((p==255) & (m==192))


predictedclear_instead_cloud = ((p==66) & (m==255))
predictedclear_instead_cloudshadow = ((p==66) & (m==129))
predictedclear_instead_semitransparent = ((p==66) & (m==192))


predictedshadow_instead_cloud = ((p==129) & (m==255))
predictedshadow_instead_clear = ((p==129) & (m==66))
predictedshadow_instead_semitransparent = ((p==129) & (m==192))


predictedsemitransparent_instead_cloud = ((p==192) & (m==255))
predictedsemitransparent_instead_clear = ((p==192) & (m==66))
predictedsemitransparent_instead_cloudshadow = ((p==192) & (m==129))


predicted_instead_undefined=((p!=3) & (m==3))
predictedundefined_instead_ = ((p==3) & (m!=3))


#We don't need to show all the labels every time; only these that are actually included
#So create a list of existing labels

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


#Now actually assing labels (1-16) to masks and map them to some color

pix=np.where(true_cloud==False, pix, 1)
pix=np.where(true_clear==False, pix, 2)
pix=np.where(true_cloudshadow==False, pix, 3)
pix=np.where(true_semitransparent==False, pix, 4)

pix=np.where(predictedcloud_instead_clear==False, pix, 5)
pix=np.where(predictedcloud_instead_cloudshadow==False, pix, 6)
pix=np.where(predictedcloud_instead_semitransparent==False, pix, 7)

pix=np.where(predictedclear_instead_cloud==False, pix, 8)
pix=np.where(predictedclear_instead_cloudshadow==False, pix, 9)
pix=np.where(predictedclear_instead_semitransparent==False, pix, 10)

pix=np.where(predictedshadow_instead_cloud==False, pix, 11)
pix=np.where(predictedshadow_instead_clear==False, pix, 12)
pix=np.where(predictedshadow_instead_semitransparent==False, pix, 13)

pix=np.where(predictedsemitransparent_instead_cloud==False, pix, 14)
pix=np.where(predictedsemitransparent_instead_clear==False, pix, 15)

pix=np.where(predictedsemitransparent_instead_cloudshadow==False, pix, 16)

pix=np.where(true_undefined==False, pix, 17)
pix=np.where(predictedundefined_instead_==False, pix, 18)
pix=np.where(predicted_instead_undefined==False, pix, 19)

label_to_color = {
    1: [255, 255,255], # True cloud: white
    2: [0, 0,0], #True clear: black
    3: [190, 190, 190], #True cloudshadow: lighter grey
    4: [100,100,100], #True semitransparent: darker grey

    5: [0,255,255], # Cloud instead of clear: aqua
    6: [0,0,255], # Cloud instead of cloud shadow: pure blue
    7: [135,206,235], # Cloud instead of semitransparent cloud : sky blue
    
    8: [0,255,0], #Clear instead of cloud: lime green
    9: [240,230,140], #Clear instead of cloudshadow: khaki
    10: [60,179,113], #Clear instead of semitransparent: mediumseagreen
    
    11: [255, 201, 0], #Shadow instead of cloud: 
    12: [255,255,0], #Shadow instead of clear: yellow
    13: [204,204,0], #Shadow instead of semitransparent: Dark yellow 1
    
    14: [240,128,128], #Semitransparent instead of cloud: lightcolar
    15: [255,0,0], #Semitransparent instead of clear: red
    16: [220,20,60], #Semitransparent instead of shadow : crimson
    
    17: [255,0,255], #True undefined : fuchsia
    18: [238,130,238], #Undefined predicted instead of sth else: violet
    19: [153,50,204] #Predicted something else instead of undefined: darkorchid
    }
    
#Create the rgb-image

rgb_img = np.zeros((*pix.shape, 3))
 
for key in label_to_color.keys():
    rgb_img[pix == key] = label_to_color[key]

im_result = Image.fromarray(np.uint8(rgb_img))


#In order to include the legend, open this image in matplotlib

gs = GridSpec(6,1)

fig = plt.figure(figsize = (10,12))
ax1 = fig.add_subplot(gs[:-1,:]) ##for the plot
ax2 = fig.add_subplot(gs[-1,:])   ##for the legend

ax1.imshow(im_result)

legend_labels=["True cloud","True clear","True cloudshadow","True semitransparent cloud","P: cloud T: clear","P: cloud T: shadow","P: cloud T: semitransparent cloud","P: clear T: cloud","P: clear T: shadow","P: clear T: semitransparent","P: shadow T: cloud","P: shadow T: clear","P: shadow T: semitransparent","P: semitransparent T: cloud","P: semitransparent T: clear","P: semitransparent T: shadow","True undefined","Undef. FP","Undef. FN"]

legend_data=[]

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

plt.savefig(input_folder+"/prediction_info.png" ,bbox_inches = 'tight',pad_inches = 0)

if(check(true_undefined)==False or check(predictedundefined_instead_)==False or check(predicted_instead_undefined)==False):
    plt.savefig(tiles_with_undefined+"/"+input_folder.split("/")[-1]+"_prediction_info.png",bbox_inches = 'tight',pad_inches = 0)
         
