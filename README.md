# seg_utils

### Segmentation utilities for the Narasimhan Lab

Available Functions:

coordinates_from_json()

mask_from_dict()

### Dependencies and Versions

cv2: version 4.2.0
PIL: version 7.1.2
numpy: 1.18.5

### Example
Python
```Python
annotation_file = 'my_JSON'
image_directory = '/path/to/folder/with/images'
destination_directory = '/path/to/destination'

coordinate_dictionary = (image_filename, annotation_file)
mask_from_dict(coordinate_dictionary, image_directory, destination_directory)

```
Command line
```
# run script
python jsonextract.py --json_path 'my_JSON' --input_dir '/path/to/folder/with/images' --dest_dir '/path/to/destination'

# optional arg --color: Produce a colored output for sanity checking purposes
python jsonextract.py --json_path 'my_JSON' --input_dir '/path/to/folder/with/images' --dest_dir '/path/to/destination' --color True

# see all required and optional args
python jsonextract.py --help
```
