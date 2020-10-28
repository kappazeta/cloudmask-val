#!/bin/bash

for dir in prediction_v3/prediction/*; do
echo $dir
for label in cloud cloudshadow clear semitransparent undefined; do
python individual_label_info.py $dir $label
done
done
