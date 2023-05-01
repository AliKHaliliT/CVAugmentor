# CVAugmentor
## Introduction
This is a simple tool to augment images and videos for computer vision tasks.

Available augmentations are:
    no_augmentation,
    flip,
    zoom,
    rotate,
    shear,
    grayscale,
    hue,
    saturation,
    brightness,
    exposure,
    blur,
    noise,
    cutout,
    negative.
## Installation
You can install the package using pip:
```bash
pip install CVAugmentor
```
## Usage
For a detailed usage guide, please refer to the [documentation](https://alikhalilit.github.io/CVAugmentor/).
### Single Image Augmentation
```python
# Importing the libraries
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

# Create a Pipeline object
p = Pipeline()

# Augment the image
p.augment(input_path="path/to/input_image", output_path="path/to/output_image", target="image", process_type="single", mode="singular", augmentations=augmentations, verbose=True, warn_verbose=True)
```
### Single Video Augmentation
```python
# Importing the libraries
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

# Create a Pipeline object
p = Pipeline()

# Augment the video
p.augment(input_path="path/to/input_video", output_path="path/to/output_video", target="video", process_type="single", mode="singular", augmentations=augmentations, verbose=True, warn_verbose=True)
```
### Augmenting Multiple Images
```python
# Importing the libraries
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

# Create a Pipeline object
p = Pipeline()

# Augment the images
p.augment(input_path="path/to/input_images", output_path="path/to/output_images", target="image", process_type="batch", mode="singular", augmentations=augmentations, verbose=True, warn_verbose=True)
```
### Augmenting Multiple Videos
```python
# Importing the libraries
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

# Create a Pipeline object
p = Pipeline()

# Augment the videos
p.augment(input_path="path/to/input_videos", output_path="path/to/output_videos", target="video", process_type="batch", mode="singular", augmentations=augmentations, verbose=True, warn_verbose=True)
```
## License
This work is licensed under an [MIT](https://choosealicense.com/licenses/mit/) License.