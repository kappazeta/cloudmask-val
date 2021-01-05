
from PIL import Image
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="path to input folder")
parser.add_argument("--which_model", required=True, choices=["s2cor", "s2cloudless"], help="path to input folder")
parser.add_argument("--name", help="(Optional) how do you want to call the resulting html file. Default is 'comparison_model'")
a = parser.parse_args()

input_folder=a.input
model=a.which_model

#Check if we have all the necessary images:

for directory in os.listdir(input_folder):
    if(os.path.isfile(input_folder+directory+"/s2cloudless_like_prediction.png")==False):
        prediction=input_folder+directory+"/prediction.png"
        with Image.open(prediction) as im:
            p = np.array(im, dtype=np.float)

        rgb_img = np.zeros((*p.shape, 3))

        p = [[255 if b==192 else b for b in i] for i in p]
        p = [[0 if b!=255 else b for b in i] for i in p]
        p_im = Image.fromarray(np.uint8(p))
        p_im.save(input_folder+directory+"/s2cloudless_like_prediction.png")

        
        rgb_img[p == 255] = [255,255,0]
        rgb_img[p != 255] = [0,0,0]
        im_result = Image.fromarray(np.uint8(rgb_img))
        im_result.save(input_folder+directory+"/prediction_yellow.png")

    if(os.path.isfile(input_folder+directory+"/s2cloudless_yellow.png")==False):

        if(os.path.isfile(input_folder+directory+"/s2cloudless.png")):
       
            s2cloudless=input_folder+directory+"/s2cloudless.png"

            with Image.open(s2cloudless) as im:
                s2cloud = np.array(im, dtype=np.float)

            rgb_img2 = np.zeros((*s2cloud.shape, 3))

            rgb_img2[s2cloud == 255] = [255,255,0]
            rgb_img2[s2cloud != 255] = [0,0,0]
            im_result2 = Image.fromarray(np.uint8(rgb_img2))
            im_result2.save(input_folder+directory+"/s2cloudless_yellow.png")
        else:
            print("S2cloudless prediction missing here: "+str(input_folder+directory))

    if(os.path.isfile(input_folder+directory+"/prediction_colors.png")==False):

        prediction=input_folder+directory+"/prediction.png"
        with Image.open(prediction) as im:
            p = np.array(im, dtype=np.float)

        rgb_img = np.zeros((*p.shape, 3))
        rgb_img[p == 255] = [255,255,0]
        rgb_img[p == 66] = [0,0,0]
        rgb_img[p == 3] = [255,0,255]
        rgb_img[p == 129] = [0,255,0]
        rgb_img[p == 192] = [0,0,255]
        im_result = Image.fromarray(np.uint8(rgb_img))
        im_result.save(input_folder+directory+"/prediction_colors.png")

    if(os.path.isfile(input_folder+directory+"/s2c_colors.png")==False):

        prediction=input_folder+directory+"/SCL.png"
        with Image.open(prediction) as im:
            p = np.array(im, dtype=np.float)

        rgb_img = np.zeros((*p.shape, 3))
        rgb_img[p == 255] = [255,255,0]
        rgb_img[p == 66] = [0,0,0]
        rgb_img[p == 3] = [255,0,255]
        rgb_img[p == 129] = [0,255,0]
        rgb_img[p == 192] = [0,0,255]
        im_result = Image.fromarray(np.uint8(rgb_img))
        im_result.save(input_folder+directory+"/s2c_colors.png")

#Create the html page

content=""

dummy=open("index_dummy.txt","r")

lines=dummy.readlines()

for line in lines:
    if("xxx" not in line and "yyy" not in line):
        content+=line
    if("xxx" in line):
        i=1
        for directory in os.listdir(input_folder):
            newline="\n$('#containerx').beforeAfter({imagePath:'js/'});"
            newline=newline.replace('x',str(i))
            content+=newline
            i=i+1
            newline="\n$('#containerx').beforeAfter({imagePath:'js/'});"
            newline=newline.replace('x',str(i))
            content+=newline
            i=i+1
    if("yyy" in line):
        i=1
        if(model=="s2cloudless"):
            for directory in os.listdir(input_folder):
                if(os.path.exists(input_folder+directory+"/prediction_yellow.png") and os.path.exists(input_folder+directory+"/s2cloudless_yellow.png")):
                    newline="<div class=\"rida\">\n<div class=\"container-outer\">TILE NR</div>\n<div class=\"container-outer\">\n<div id=\"containerx\">\n<div class=\"img2\"><img alt=\"before\" src=\"prediction_source\" width=\"512\" height=\"512\" /></div>\n<div><img alt=\"after\" src=\"orig_source\" width=\"512\" height=\"512\" /></div>\n</div>\n</div>\n\n"
                    newline=newline.replace("x",str(i))
                    newline=newline.replace("TILE NR",directory)
                    newline=newline.replace("orig_source",input_folder+directory+"/orig.png")
                    newline=newline.replace("prediction_source",input_folder+directory+"/prediction_yellow.png")
                    content+=newline
                    i=i+1
                    newline="<div class=\"container-outer\">\n<div id=\"containerx\">\n<div class=\"img2\"><img alt=\"before\" src=\"s2cloudless_source\" width=\"512\" height=\"512\" /></div>\n<div><img alt=\"after\" src=\"orig_source\" width=\"512\" height=\"512\" /></div>\n</div>\n</div>\n</div><br><br><br>\n"
                    newline=newline.replace("x",str(i))
                    newline=newline.replace("orig_source",input_folder+directory+"/orig.png")
                    newline=newline.replace("s2cloudless_source",input_folder+directory+"/s2cloudless_yellow.png")
                    content+=newline
                    i=i+1

        if(model=="s2cor"):
            for directory in os.listdir(input_folder):
                if(os.path.exists(input_folder+directory+"/prediction_yellow.png") and os.path.exists(input_folder+directory+"/s2cloudless_yellow.png")):
                    newline="<div class=\"rida\">\n<div class=\"container-outer\">TILE NR</div>\n<div class=\"container-outer\">\n<div id=\"containerx\">\n<div class=\"img2\"><img alt=\"before\" src=\"prediction_source\" width=\"512\" height=\"512\" /></div>\n<div><img alt=\"after\" src=\"orig_source\" width=\"512\" height=\"512\" /></div>\n</div>\n</div>\n\n"
                    newline=newline.replace("x",str(i))
                    newline=newline.replace("TILE NR",directory)
                    newline=newline.replace("orig_source",input_folder+directory+"/orig.png")
                    newline=newline.replace("prediction_source",input_folder+directory+"/prediction_colors.png")
                    content+=newline
                    i=i+1
                    newline="<div class=\"container-outer\">\n<div id=\"containerx\">\n<div class=\"img2\"><img alt=\"before\" src=\"s2cloudless_source\" width=\"512\" height=\"512\" /></div>\n<div><img alt=\"after\" src=\"orig_source\" width=\"512\" height=\"512\" /></div>\n</div>\n</div>\n</div><br><br><br>\n"
                    newline=newline.replace("x",str(i))
                    newline=newline.replace("orig_source",input_folder+directory+"/orig.png")
                    newline=newline.replace("s2cloudless_source",input_folder+directory+"/s2c_colors.png")
                    content+=newline
                    i=i+1

if(a.name!=None):
    name=a.name+"_"+model
else:
    name="Comparison_"+model
f=open(name+".html","w")
f.write(content)
f.close


    

