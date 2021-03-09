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
parser.add_argument("--model", required=True, choices=["all","S2C","s2cloudless","fmask"], help="which model we want to compare against prediction.png")

a = parser.parse_args()
input_folder=a.input

predict=input_folder+'/prediction.png'
mask=input_folder+'/label.png'

other_models=[]

if(a.model=="all"):
    s2c=input_folder+'/SCL.png'
    fmask=input_folder+'/FMC.png'
    s2cloudless=input_folder+'/SS2C_sinergise.png'
    other_models.append(s2c)
    other_models.append(fmask)
    other_models.append(s2cloudless)

if(a.model=="S2C"):
    other_model=input_folder+'/SCL.png'
    other_models.append(other_model)

if(a.model=="s2cloudless"):
    other_model=input_folder+'/SS2C_sinergise.png'
    other_models.append(other_model)

if(a.model=="fmask"):
    other_model=input_folder+'/FMC.png'
    other_models.append(other_model)


#Pixel values:
#3 - undefined
#66 - clear
#129 - cloud shadow
#192 - semitransparent
#255 - cloud

#Pixel values for s2cloudless:
#255 - cloud
#0 - non-cloud


with Image.open(mask) as im:
    m = np.array(im, dtype=np.float)
    pix = np.array(im, dtype=np.float)
    
with Image.open(predict) as im:
    p = np.array(im, dtype=np.float)

for other_model in other_models:

    with Image.open(other_model) as im:
        p2 = np.array(im, dtype=np.float)


    #Create masks:

    #both true

    p_cloud_s_cloud_true=((p==255) & (p2==255) & (m==255))
    p_clear_s_clear_true=((p==66) & (p2==66) & (m==66))
    p_shadow_s_shadow_true=((p==129) & (p2==129) & (m==129))
    p_semi_s_semi_true=((p==192) & (p2==192) & (m==192))
    p_undef_s_sundef_true=((p==3) & (p2==3) & (m==3))
    p_undef_s_missing_true=((p==20) & (p2==20) & (m==20))

    if("SS2C_sinergise" in other_model):
        p_cloud_s_cloud_true_2=((p==192) & (p2==255) & (m==192))
        p_clear_s_clear_true_2=((p==129) & (p2==66) & (m==129))
        p_clear_s_clear_true_3=((p==3) & (p2==66) & (m==3))
        p_clear_s_clear_true_4=((p==20) & (p2==66) & (m==20))

    #both false

    both_false=((p!=m) & (p2!=m))

    if("SS2C_sinergise" in other_model):
        both_false=(((p==255) | (p==192)) & (m!=255) & (m!=192) & (p2==255))
        both_false_2=((p!=255) & (p!=192) & ((m==255) | (m==192)) & (p2!=255))

    #Prediction true, other model false

    p_true_s_false = ((p==m) & (p2 != m))

    if("SS2C_sinergise" in other_model):
        p_true_s_false=(((p==255) | (p==192)) & ((m==255) | (m!=192)) & (p2!=255))
        p_true_s_false_2=((p!=255) & (p!=192) & (m!=255) & (m!=192) & (p2==255))

    #other model true, prediction false

    p_false_s_true = ((p!=m) & (p2 == m))

    if("SS2C_sinergise" in other_model):
        p_false_s_true=(((p==255) | (p==192)) & (m!=255) & (m!=192) & (p2!=255))
        p_false_s_true_2=((p!=255) & (p!=192) & ((m==255) | (m==192)) & (p2==255))

    #Now assing labels to masks and map them to some color

    pix=np.where(p_cloud_s_cloud_true==False, pix, 1)
    pix=np.where(p_clear_s_clear_true==False, pix, 2)
    pix=np.where(p_shadow_s_shadow_true==False, pix, 3)
    pix=np.where(p_undef_s_sundef_true==False, pix, 4)
    pix=np.where(p_semi_s_semi_true==False, pix, 5)
    pix=np.where(both_false==False, pix, 6)
    pix=np.where(p_true_s_false==False, pix, 7)
    pix=np.where(p_false_s_true==False, pix, 8)

    if("SS2C_sinergise" in other_model):
        pix=np.where(p_cloud_s_cloud_true_2==False, pix, 9)
        pix=np.where(p_clear_s_clear_true_2==False, pix, 10)
        pix=np.where(p_clear_s_clear_true_3==False, pix, 11)
        pix=np.where(p_clear_s_clear_true_4==False, pix, 12)
        pix=np.where(both_false_2==False, pix, 13)
        pix=np.where(p_true_s_false_2==False, pix, 14)
        pix=np.where(p_false_s_true_2==False, pix, 15)
  


    label_to_color = {
        1: [255, 255,255], # True cloud: white
        2: [66, 66,66], #True clear: black
        3: [129, 129, 129], #True cloudshadow: lighter grey
        4: [3,3,3], #True undefined
        5: [192,192,192], # True semitransparent
        6: [153,50,204], # Both false
        7: [0,255,0], # Prediction true, sen2cor false
        8: [255,0,0], #S2cor true, prediction false
        9: [255, 255,255],
        10: [66, 66,66],
        11: [66, 66,66],
        12: [66, 66,66],
        13: [153,50,204],
        14: [0,255,0],
        15: [255,0,0]
        }
    
    #Create the rgb-image

    rgb_img = np.zeros((*pix.shape, 3))
 
    for key in label_to_color.keys():
        rgb_img[pix == key] = label_to_color[key]

    im_result = Image.fromarray(np.uint8(rgb_img))

    other_name=other_model.split("/")[-1].split(".png")[0]

    im_result.save(input_folder+"/"+other_name+"_comparison.png")

    
