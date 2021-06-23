# seg_utils: Segmentation utilities for the Narasimhan Lab

### Main Functions:

Prep a mask file from a JSON annotation: 
```
coordinates_from_json()

mask_from_dict()
```

Evaluate the performance of a segmentation model or two annotators

```
pixel_accuracy()

mean_accuracy()

mean_IU()

frequency_weighted_IU()
```

### Dependencies and Versions

cv2: version 4.2.0

PIL: version 7.1.2

numpy: version 1.18.5

scikit-image: version 0.18.1

### Example 
#### jsonextract

Command line
```
# run script
python jsonextract.py --json_path 'my_JSON' --input_dir '/path/to/folder/with/images' --dest_dir '/path/to/destination'

# optional arg --color: Produce a colored output for sanity checking purposes
python jsonextract.py --json_path 'my_JSON' --input_dir '/path/to/folder/with/images' --dest_dir '/path/to/destination' --color True

# see all required and optional args
python jsonextract.py --help
```
#### interp-metrics

Command line

```
# run script 
python interp-metrics.py --y_true path/to/ground_truth --y_pred path/to/prediction 
# output
{'Filename': 'prediction.png', 'Pixel Accuracy': 1.0, 'Mean IOU': 1.0, 'Individual Polygon IOUs': [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}

# optional arg - polygon
# Used for formatting per polygon IOU array into dict linking each polygon with its score

python interp-metrics.py --y_true path/to/ground_truth --y_pred path/to/prediction --polygon spine
# output 
{'Filename': 'prediction.png', 'Pixel Accuracy': 1.0, 'Mean IOU': 1.0, 'Individual Polygon IOUs': {'T12': 1.0, 'L1': 1.0, 'L2': 1.0, 'L3': 1.0, 'L4': 1.0, 'L5': 1.0}}
