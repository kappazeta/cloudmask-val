import sys
import os


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="path to prediction folder of experiment")
parser.add_argument("--output", required=True, help="path to experiment folder")
a = parser.parse_args()
input=a.input
output_folder=a.output

#input="/home/heido/cloudmask/big_image/prediction/"



content="<style> table, th, td { border: 1px solid black; table-layout: fixed; overflow: auto; width: 130%;}</style><table><tr><th style=\"width: 90px\">Tile nr</th><th style=\"width: 520px\">Original</th><th style=\"width: 520px\">Label</th><th style=\"width: 520px\">Prediction</th><th style=\"width: 520px\">Prediction info</th><th style=\"width: 520px\">S2c comparison</th></tr>"

for folder in os.listdir(input):
    tile_name=folder.split("_")[0]+"_\n"+folder.split("_")[1].split("T")[0]+"\nT"+folder.split("_")[1].split("T")[1]+"_\ntile_"+folder.split("_")[3]+"_"+folder.split("_")[4]
    dir=input+"/"+folder
    original=dir+"/orig.png"
    label=dir+"/label.png"
    prediction=dir+"/prediction.png"
    prediction_info=dir+"/prediction_info.png"
    s2cc=dir+"/s2c_comparison.png"
    content=content+"<tr><td>"+tile_name+"</td><td><img src='"+original+"'></td><td><img src='"+label+"'></td><td><img src='"+prediction+"'></td><td><img src='"+prediction_info+"'></td><td><img src='"+s2cc+"'></td><tr>"
    
file2 = open(output_folder+"/images.html","w") 
file2.write(content)
file2.close() 
