#!/bin/bash

input=$1

folders=()

#Read the file contents into name, description and data folder arrays:

while read line; do

if [[ "$line" == *"folder"* ]]; then
  IFS=':' read -ra ADDR <<< "$line"
  folders+=(${ADDR[1]})
fi
done < $input

len=${#folders[@]}
nr="$((len - 1))"

for (( i=0; i<=$nr; i++ ))
do  

   prediction="${folders[i]}/prediction"
   
   for dir in $prediction/*; do
   
    
    prediction_info_file="${dir}/prediction_info.png"
    s2c_comparison_file="${dir}/s2c_comparison.png"
    
    if test -f "$prediction_info_file"; then
      a=1
    else
      echo $dir
      python create_prediction_info.py --input $dir
    fi
    
    if test -f "$s2c_comparison_file"; then
      a=1
    else

      python sen2cor_mask_vs_prediction.py --input $dir
    fi
    done
    python tiles.py --input $prediction --output "${folders[i]}"
        
done

python create_html.py --info $input




