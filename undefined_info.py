import sys
import os
import cv2
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
from matplotlib import cm

input_folder="prediction_v1/prediction/"

predicted_undefined_pixels=0

p_undef_t_cloud_p=0
p_undef_t_clear_p=0
p_undef_t_shadow_p=0
p_undef_t_semitransparent_p=0
p_undef_t_undef_p=0

true_undefined_pixels=0

t_undef_p_cloud_p=0
t_undef_p_clear_p=0
t_undef_p_shadow_p=0
t_undef_p_semitransparent_p=0

for folder in os.listdir(input_folder):
    input_folder=input_folder+folder
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
        
    p_undef_t_cloud=((undefinedp>clearp) & (undefinedp>cloudshadowp) & (undefinedp>semitransparentp) & (undefinedp>cloudp) & (cloudm==255))
    p_undef_t_clear=((undefinedp>clearp) & (undefinedp>cloudshadowp) & (undefinedp>semitransparentp) & (undefinedp>cloudp) & (clearm==255))
    p_undef_t_shadow=((undefinedp>clearp) & (undefinedp>cloudshadowp) & (undefinedp>semitransparentp) & (undefinedp>cloudp) & (cloudshadowm==255))
    p_undef_t_semitransparent=((undefinedp>clearp) & (undefinedp>cloudshadowp) & (undefinedp>semitransparentp) & (undefinedp>cloudp) & (semitransparentm==255))
    p_undef_t_undef=((undefinedp>clearp) & (undefinedp>cloudshadowp) & (undefinedp>semitransparentp) & (undefinedp>cloudp) & (undefinedm==255))
    
    t_undef_p_cloud=((cloudp>clearp) & (cloudp>cloudshadowp) & (cloudp>semitransparentp) & (cloudp>undefinedp) & (undefinedm==255))
    t_undef_p_clear=((clearp>cloudp) & (clearp>cloudshadowp) & (clearp>semitransparentp) & (clearp>undefinedp) & (undefinedm==255))
    t_undef_p_shadow=((cloudshadowp>clearp) & (cloudshadowp>cloudp) & (cloudshadowp>semitransparentp) & (cloudshadowp>undefinedp) & (undefinedm==255))
    t_undef_p_semitransparent=((semitransparentp>clearp) & (semitransparentp>cloudshadowp) & (semitransparentp>cloudp) & (semitransparentp>undefinedp) & (undefinedm==255))
    
    
    predicted_undefined_pixels+=np.sum(p_undef_t_cloud)+np.sum(p_undef_t_clear)+np.sum(p_undef_t_shadow)+np.sum(p_undef_t_semitransparent)+np.sum(p_undef_t_undef)

    p_undef_t_cloud_p+=np.sum(p_undef_t_cloud)
    p_undef_t_clear_p+=np.sum(p_undef_t_clear)
    p_undef_t_shadow_p+=np.sum(p_undef_t_shadow)
    p_undef_t_semitransparent_p+=np.sum(p_undef_t_semitransparent)
    p_undef_t_undef_p+=np.sum(p_undef_t_undef)

    true_undefined_pixels+=np.sum(t_undef_p_cloud)+np.sum(t_undef_p_clear)+np.sum(t_undef_p_shadow)+np.sum(t_undef_p_semitransparent)+np.sum(p_undef_t_undef)

    t_undef_p_cloud_p+=np.sum(t_undef_p_cloud)
    t_undef_p_clear_p+=np.sum(t_undef_p_clear)
    t_undef_p_shadow_p+=np.sum(t_undef_p_shadow)
    t_undef_p_semitransparent_p+=np.sum(t_undef_p_semitransparent)
    
    input_folder="prediction_v1/prediction/"


    
print(true_undefined_pixels)
print("If mask is undefined, model predicts clouds "+str(t_undef_p_cloud_p/true_undefined_pixels*100)+" %")
print("If mask is undefined, model predicts clear "+str(t_undef_p_clear_p/true_undefined_pixels*100)+" %")
print("If mask is undefined, model predicts shadow "+str(t_undef_p_shadow_p/true_undefined_pixels*100)+" %")
print("If mask is undefined, model predicts semitransparent "+str(t_undef_p_semitransparent_p/true_undefined_pixels*100)+" %")
print("If mask is undefined, model predicts undefined "+str(p_undef_t_undef_p/true_undefined_pixels*100)+" %")

print("If prediction is undefined, target was clouds "+str(p_undef_t_cloud_p/predicted_undefined_pixels*100)+" %")
print("If prediction is undefined, target was clear "+str(p_undef_t_clear_p/predicted_undefined_pixels*100)+" %")
print("If prediction is undefined, target was shadow "+str(p_undef_t_shadow_p/predicted_undefined_pixels*100)+" %")
print("If prediction is undefined, target was semitransparent "+str(p_undef_t_semitransparent_p/predicted_undefined_pixels*100)+" %")
print("If prediction is undefined, target was undefined "+str(p_undef_t_undef_p/predicted_undefined_pixels*100)+" %")


    
    
    

    
    
    
    
    
        
   
