# seg_utils

TODO: Improve Documentation
* create a new demo.ipynb for the new jsonextract script
* add to documentation information about required and optional args

Segmentation utilities for the Narasimhan Lab

Available Functions:

coordinates_from_json()

mask_from_dict()

### Example
```Python
annotation_file = 'my_JSON'
image_directory = '/path/to/folder/with/images'
destination_directory = '/path/to/destination'

coordinate_dictionary = (image_filename, annotation_file)
mask_from_dict(coordinate_dictionary, image_directory, destination_directory)

```
#### See a more detailed example in the "demo.ipynb" example Jupyter Notebook.
