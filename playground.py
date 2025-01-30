# Single Image Augmentation
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


## Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

## Create a Pipeline object
p = Pipeline()

## Augment the image
p.augment(input_path="path/to/input_image", 
          output_path="path/to/output_image", 
          target="image", 
          process_type="single", 
          mode="singular", 
          augmentations=augmentations, 
          aug_verbose=True)


# Single Video Augmentation
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


## Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

## Create a Pipeline object
p = Pipeline()

## Augment the video
p.augment(input_path="path/to/input_video", 
          output_path="path/to/output_video", 
          target="video", 
          process_type="single", 
          mode="singular", 
          augmentations=augmentations, 
          aug_verbose=True)


# Augmenting Multiple Images
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


## Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

## Create a Pipeline object
p = Pipeline()

## Augment the images
p.augment(input_path="path/to/input_images", 
          output_path="path/to/output_images", 
          target="image", 
          process_type="batch", 
          mode="singular", 
          augmentations=augmentations, 
          verbose=True, 
          warn_verbose=True)


# Augmenting Multiple Videos
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


## Define the augmentations
augmentations = {
    "zoom": aug.zoom(),
    "flip": aug.flip(),
}

## Create a Pipeline object
p = Pipeline()

## Augment the videos
p.augment(input_path="path/to/input_videos", 
          output_path="path/to/output_videos", 
          target="video", 
          process_type="batch", 
          mode="singular", 
          augmentations=augmentations, 
          verbose=True, 
          warn_verbose=True)