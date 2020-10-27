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

cloud_predict=input_folder+'/predict_CLOUD.png'
cloud_mask=input_folder+'/CLOUD.png'

cloudshadow_predict=input_folder+'/predict_CLOUD_SHADOW.png'
cloudshadow_mask=input_folder+'/CLOUD_SHADOW.png'

clear_predict=input_folder+'/predict_CLEAR.png'
clear_mask=input_folder+'/CLEAR.png'

semitransparent_predict=input_folder+'/predict_SEMI_TRANSPARENT_CLOUD.png'
semitransparent_mask=input_folder+'/SEMI_TRANSPARENT_CLOUD.png'

undefined_predict=input_folder+'/predict_UNDEFINED.png'
undefined_mask=input_folder+'/UNDEFINED.png'
            
#Read in the mask files and make them numpy arrays

with Image.open(cloud_mask) as im:
    cloudm = np.array(im, dtype=np.float)
    
with Image.open(cloudshadow_mask) as im:
    cloudshadowm = np.array(im, dtype=np.float)
    
with Image.open(clear_mask) as im:
    clearm = np.array(im, dtype=np.float)
    
with Image.open(semitransparent_mask) as im:
    semitransparentm = np.array(im, dtype=np.float)
    
with Image.open(undefined_mask) as im:
    undefinedm = np.array(im, dtype=np.float)
    
#Read in predict files    

with Image.open(cloud_predict) as im:
    pix = np.array(im, dtype=np.float)
    cloudp = np.array(im, dtype=np.float)
    
with Image.open(cloudshadow_predict) as im:
    cloudshadowp = np.array(im, dtype=np.float)
    
with Image.open(clear_predict) as im:
    clearp = np.array(im, dtype=np.float)
    
with Image.open(semitransparent_predict) as im:
    semitransparentp = np.array(im, dtype=np.float)
    
with Image.open(undefined_predict) as im:
    undefinedp = np.array(im, dtype=np.float)
    
#Both undefined label and undefined prediction are problematic

problem=(undefinedm==255)
problem2=((undefinedp>clearp) & (undefinedp>cloudshadowp) & (undefinedp>semitransparentp) & (undefinedp>cloudp))
   
#Create masks which show all possible true and false predictions (and if false, then what was true)

true_cloud=((cloudp>clearp) & (cloudp>cloudshadowp) & (cloudp>semitransparentp) & (cloudm==255))

true_clear=((clearp>cloudp) & (clearp>cloudshadowp) & (clearp>semitransparentp) & (clearm==255))

true_cloudshadow=((cloudshadowp>cloudp) & (cloudshadowp>clearp) & (cloudshadowp>semitransparentp) & (cloudshadowm==255))

true_semitransparent=((semitransparentp>cloudp) & (semitransparentp>clearp) & (semitransparentp>cloudshadowp) & (semitransparentm==255))

true_undefined=((semitransparentp>cloudp) & (semitransparentp>clearp) & (semitransparentp>cloudshadowp) & (semitransparentm==255))

predictedcloud_instead_clear = ((cloudp>clearp) & (cloudp>cloudshadowp) & (cloudp>semitransparentp) & (clearm==255))
predictedcloud_instead_cloudshadow=((cloudp>clearp) & (cloudp>cloudshadowp) & (cloudp>semitransparentp) & (cloudshadowm==255))
predictedcloud_instead_semitransparent=((cloudp>clearp) & (cloudp>cloudshadowp) & (cloudp>semitransparentp) & (semitransparentm==255))

predictedclear_instead_cloud = ((clearp>cloudp) & (clearp>cloudshadowp) & (clearp>semitransparentp) & (cloudm==255))
predictedclear_instead_cloudshadow = ((clearp>cloudp) & (clearp>cloudshadowp) & (clearp>semitransparentp) & (cloudshadowm==255))
predictedclear_instead_semitransparent = ((clearp>cloudp) & (clearp>cloudshadowp) & (clearp>semitransparentp) & (semitransparentm==255))

predictedshadow_instead_cloud = ((cloudshadowp>cloudp) & (cloudshadowp>clearp) & (cloudshadowp>semitransparentp) & (cloudm==255))
predictedshadow_instead_clear = ((cloudshadowp>cloudp) & (cloudshadowp>clearp) & (cloudshadowp>semitransparentp) & (clearm==255))
predictedshadow_instead_semitransparent = ((cloudshadowp>cloudp) & (cloudshadowp>clearp) & (cloudshadowp>semitransparentp) & (semitransparentm==255))

predictedsemitransparent_instead_cloud = ((semitransparentp>cloudp) & (semitransparentp>clearp) & (semitransparentp>cloudshadowp) & (cloudm==255))
predictedsemitransparent_instead_clear = ((semitransparentp>cloudp) & (semitransparentp>clearp) & (semitransparentp>cloudshadowp) & (clearm==255))

predictedsemitransparent_instead_cloudshadow = ((semitransparentp>cloudp) & (semitransparentp>clearp) & (semitransparentp>cloudshadowp) & (cloudshadowm==255))


#We don't need to show all the labels every time; only these that are actually included
#So create a list of existing labels

existing_labels=[]

#Return False if all elements are True

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
if(check(problem)==False):
    existing_labels.append(17)
if(check(problem2)==False):
    existing_labels.append(18)

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

pix=np.where(problem==False, pix, 17)
pix=np.where(problem2==False, pix, 18)

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
    
    11: [65,105,225], #Shadow instead of cloud: royal blue
    12: [255,255,0], #Shadow instead of clear: yellow
    13: [204,204,0], #Shadow instead of semitransparent: Dark yellow 1
    
    14: [138,43,226], #Semitransparent instead of cloud: blue violet
    15: [178,34,34], #Semitransparent instead of clear: firebrick
    16: [34,139,34], #Semitransparent instead of shadow : forestgreen
    
    17: [237, 14, 222], #Undefined area: instead of shadow : ugly purple
    18: [203, 14, 237] #Undefined area: instead of shadow : ugly purple 2
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

legend_labels=["True cloud","True clear","True cloudshadow","True semitransparent cloud","P: cloud T: clear","P: cloud T: shadow","P: cloud T: semitransparent cloud","P: clear T: cloud","P: clear T: shadow","P: clear T: semitransparent","P: shadow T: cloud","P: shadow T: clear","P: shadow T: semitransparent","P: semitransparent T: cloud","P: semitransparent T: clear","P: semitransparent T: shadow","T: undefined","P:undefined"]

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

if(check(problem)==False):
    plt.savefig("prediction_v1/problematic_tiles/"+input_folder.split("/")[-1]+"_prediction_info.png",bbox_inches = 'tight',pad_inches = 0)

if(check(problem2)==False):
    plt.savefig("prediction_v1/tiles_where_undefined_is_predicted/"+input_folder.split("/")[-1]+"_prediction_info.png",bbox_inches = 'tight',pad_inches = 0)
    
         
