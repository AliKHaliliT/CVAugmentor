# Single Image Augmentation
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "blur": aug.Blur(2.5),
    "brightness": aug.Brightness(0.25),
    "cutout": aug.Cutout(max_size=64, max_count=6),
    "expsure": aug.Exposure(0.3),
    "flip": aug.Flip(),
    "grayscale": aug.Grayscale(),
    "hue": aug.Hue(-360),
    "negative": aug.Negative(),
    "no_augmentation": aug.NoAugmentation(),
    "noise": aug.Noise(0.4),
    "rotate": aug.Rotate(),
    "saturation": aug.Saturation(0.5),
    "shear": aug.Shear((0.2, 0.2)),
    "zoom": aug.Zoom(),
}


# Create a Pipeline object
p = Pipeline()

# Augment the image
p.augment(input_path="local_util_resources/samples/images/0.png", 
          output_path="local_util_resources/experiments/single_image/0.png", 
          target="image", 
          process_type="single", 
          mode="sequential", 
          augmentations=augmentations, 
          aug_verbose=True)


# Single Video Augmentation
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "blur": aug.Blur(2.5),
    "brightness": aug.Brightness(0.25),
    "cutout": aug.Cutout(max_size=64, max_count=6),
    "expsure": aug.Exposure(0.3),
    "flip": aug.Flip(),
    "grayscale": aug.Grayscale(),
    "hue": aug.Hue(-360),
    "negative": aug.Negative(),
    "no_augmentation": aug.NoAugmentation(),
    "noise": aug.Noise(0.4),
    "rotate": aug.Rotate(),
    "saturation": aug.Saturation(0.5),
    "shear": aug.Shear((0.2, 0.2)),
    "zoom": aug.Zoom(),
}


# Create a Pipeline object
p = Pipeline()

# Augment the video
p.augment(input_path="local_util_resources/samples/videos/0.mp4", 
          output_path="local_util_resources/experiments/single_video/0.mp4", 
          target="video", 
          process_type="single", 
          mode="singular", 
          augmentations=augmentations, 
          aug_verbose=True)


# Augmenting Multiple Images
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "blur": aug.Blur(),
    "brightness": aug.Brightness(),
    "cutout": aug.Cutout(),
    "expsure": aug.Exposure(),
    "flip": aug.Flip(),
    "grayscale": aug.Grayscale(),
    "hue": aug.Hue(),
    "negative": aug.Negative(),
    "no_augmentation": aug.NoAugmentation(),
    "noise": aug.Noise(),
    "rotate": aug.Rotate(),
    "saturation": aug.Saturation(),
    "shear": aug.Shear(),
    "zoom": aug.Zoom(),
}


# Create a Pipeline object
p = Pipeline()

# Augment the images
p.augment(input_path="local_util_resources/samples/images", 
          output_path="local_util_resources/experiments/multi_image", 
          target="image", 
          process_type="batch", 
          mode="singular", 
          augmentations=augmentations, 
          verbose=True, 
          warn_verbose=True,
          random_state=True)


# Augmenting Multiple Videos
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


# Define the augmentations
augmentations = {
    "blur": aug.Blur(),
    "brightness": aug.Brightness(),
    "cutout": aug.Cutout(),
    "expsure": aug.Exposure(),
    "flip": aug.Flip(),
    "grayscale": aug.Grayscale(),
    "hue": aug.Hue(),
    "negative": aug.Negative(),
    "no_augmentation": aug.NoAugmentation(),
    "noise": aug.Noise(),
    "rotate": aug.Rotate(),
    "saturation": aug.Saturation(),
    "shear": aug.Shear(),
    "zoom": aug.Zoom(),
}


# Create a Pipeline object
p = Pipeline()

# Augment the videos
p.augment(input_path="local_util_resources/samples/videos", 
          output_path="local_util_resources/experiments/multi_video", 
          target="video", 
          process_type="batch", 
          mode="singular", 
          augmentations=augmentations, 
          verbose=True, 
          aug_verbose=True,
          warn_verbose=True,
          random_state=True)