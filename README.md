# seg_utils
Segmentation utilities for the Narasimhan Lab

TODO: Improve Documentation

Class = Mask

Available Functions:

annotDict() = get annotation dictionary from JSON

getShapes() = get size of the image in pixels necessary to create the empty mask that the polygons will be "drawn onto"

get_shape_attributes() = get the attributes of the shapes (x and y coordinates for each polygon in the annotation file) as well as the labels for each polygon

drawMask() = draws a mask file from the polygon annotations, and then saves this mask as a png file

### Example
```Python
annotation_file = 'my_JSON'
image_directory = '/path/to/folder/with/images'
output_filename = 'myOutput'

myMask = Mask(annotation_file, image_directory, output_filename)

json2dictionary = myMask.annotDict()

mask = myMask.drawMask()
```

#### See a more detailed example of the json2mask module in the "demo.ipynb" example Jupyter Notebook.
