# seg_utils

TODO: Improve Documentation
* create a new demo.ipynb for the new jsonextract script
* add to documentation information about required and optional args

Segmentation utilities for the Narasimhan Lab

Available Functions:

coordinates_from_json()

mask_from_dict()

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

# see all required and optional args
python jsonextract.py --help
```
#### See a more detailed example in the "demo.ipynb" example Jupyter Notebook.
