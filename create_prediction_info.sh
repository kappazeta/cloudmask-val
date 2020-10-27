#!/bin/bash

for dir in prediction_v1/prediction/*; do
echo $dir
python create_prediction_info.py $dir
done
