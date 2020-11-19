import codecs
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--info", required=True, help="the same txt file that was given as argument to validation.sh")
a = parser.parse_args()

names=[]
folders=[]
descriptions=[]

f = open(a.info, "r")
for line in f:
  if("Experiment name" in line.split(":")[0]):
      names.append(line.split(":")[1].rstrip())
  if("Experiment description" in line.split(":")[0]):
      descriptions.append(line.split(":")[1].rstrip())
  if("Data folder" in line.split(":")[0]):
      folders.append(line.split(":")[1].rstrip().strip())

content="<style> table, th, td { border: 1px solid black; table-layout: fixed; overflow: auto; width: 130%;}</style><table><tr><th style=\"width: 300px\">Experiment</th><th style=\"width: 500px\">Confusion matrix</th><th style=\"width: 500px\">Accuracy</th><th style=\"width: 500px\">Precision</th><th style=\"width: 500px\">Recall</th><th style=\"width: 500px\">Meaniou</th><th style=\"width: 500px\">Loss</th><th style=\"width: 500px\">F1</th></tr>"

for i in range(0,len(names)):
    accuracy=codecs.open(folders[i]+"/plots/cat_accuracy.html", 'r')
    accuracy_data = accuracy.read()

    loss=codecs.open(folders[i]+"/plots/loss.html", 'r')
    loss_data = loss.read()

    recall=codecs.open(folders[i]+"/plots/recall.html", 'r')
    recall_data = recall.read()

    meaniou=codecs.open(folders[i]+"/plots/mean_io_u.html", 'r')
    meaniou_data = meaniou.read()

    precision=codecs.open(folders[i]+"/plots/precision.html", 'r')
    precision_data = precision.read()

    confusion_matrix_src=folders[i]+"/plots/confusion_matrix_plot.png"

    f1=codecs.open(folders[i]+"/plots/f1.html", 'r')
    f1_data = f1.read()
    
    content+="<tr style=\"height: 400px\"><td><b>"+names[i]+"</b><br>"+descriptions[i]+"<br><a href=\""+folders[i]+"/images.html\">Link to images</a></td><td><img src=\""+confusion_matrix_src+"\" width=\"400\" height=\"400\"></td><td>"+accuracy_data+"</td><td>"+precision_data+"</td><td width=\"400\">"+recall_data+"</td><td>"+meaniou_data+"</td><td>"+loss_data+"</td><td>"+f1_data+"</td></tr>"

content+="</table>"
    
val_file = open("validation.html","w") 
val_file.write(content)
val_file.close() 
    

