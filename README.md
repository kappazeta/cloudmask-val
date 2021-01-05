### Data requirements

The main validation script is validation.sh, which needs one txt file as an argument (the example is given as `info.txt`).

In this text file, each experiment must be represented by three consecutive lines:

    Experiment name: ...
    Experiment description: ...
    Data folder: ...

It is important that the parts before colon stay exactly as they are.
Different experiments may be separated by an empty line or by some other marker (such as `***` in the example), but need not be.

It is expected that the data folder has following contents:

1. directory `plots`, which contains following files: `cat_accuracy.html`, `f1.html`,  `loss.html`,  `mean_io_u.html`,  `precision.html`,  `recall.html`, `confusion_matrix_plot.png`
2. directory `prediction`, which contains a directory for each tile, each of which contains following images: `orig.png`, `label.png`, `prediction.png`, `SCL.png`

### Description of validation.sh script

`validation.sh` will first go thorugh each experiment's prediction folder, and (using `create_prediction_info.py` and `sen2cor_mask_vs_prediction.py`) will add two images to the directory of every tile:

1. `prediction_info.png`, which shows with a color legend where and how exactly prediction differs from the labels
2. `s2c_comparison.png`, which shows
**a)** where both models were accurate, with the same color codes as `label.png` and `prediction.png`
**b)** where prediction was right, but s2c was wrong (green),
**c)** where s2c was right and our prediction was wrong (red)
**d)** where both models were wrong (purple)

`validation.sh` will check for each tile whether these png files already exist or not, and will not start creating them again each time validation.sh is run.

Next `validation.sh` will create images.html for each experiment in the corresponding experiment folder, where for each tile `orig.png`, `label.png`, `prediction.png`, `prediction_info.png` and `s2c_comparison.png` are shown side by side.

As the last step `validation.sh` will create `validation.html` (in the same folder where the validation code is run), where each experiment's name and description is put into a table, followed by the plots in the plots directory.
Also link to each experiments `images.html` is given.

### Other validation scripts

`create_prediction_info.py` and `sen2cor_mask_vs_prediction.py` can be run separately as well.
It is useful to do if for example if you want to save tiles, where undefined values are present, to some separate folder.
It is most convenient to run these scripts correspondingly with the shell scripts `create_prediction_info.sh` and `sen2cor_mask_vs_prediction.sh`.

`image_interactive.py` takes as an argument the big image (merged from the tiles).
There it is possible to see the particular tile number by hovering the cursor over interested area.
The code also shows pixel information (replacing the color legend).
The arguments needed to run `image_interactive.py` are described in the beginning of the code.

`pixel_probability_info.py` requires as an argument path to one particular sub-tile folder, where the following files are located: predict_UNDEFINED.png, predict_CLEAR.png, predict_CLOUD_SHADOW.png, predict_SEMI_TRANSPARENT_CLOUD.png and predict_CLOUD.png, which map the model's confidence for each of the classes over given area, and prediction.png. The result will be an interactive matplotlib window, where, by hovering mouse over the pixels in prediction.png, the probability (in per centage) will be displayed for each class.

`slider_comparison.py` will create an html page with two columns of slider images. In each slider image, the bottom layer is the original satellite image, and the top layer is the prediction mask: yellow shows where cloud is predicted, and respectively black for clear, blue for semitransparent, green for cloudshadow and purple for undefined. The opacity of the top layer is set to 0.2. In the left column the prediction from kappazeta's cloudmask is used, and in the right column the same prediction from some other model that we want to compare. The script rewuires two arguments: path to prediction folder (the folder which contains the sub-tile folders) and the name of the model that we want to compare sith (currently s2cor and s2cloudless are supported).


