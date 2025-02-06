# # Single Image Augmentation
# from CVAugmentor import Augmentations as aug
# from CVAugmentor import Pipeline


# ## Define the augmentations
# augmentations = {
#     "zoom": aug.Zoom(),
#     "flip": aug.Flip(),
# }

# ## Create a Pipeline object
# p = Pipeline()

# ## Augment the image
# p.augment(input_path="util_resources/samples/images/0.jpg", 
#           output_path="util_resources/experiments/single_image/0.jpg", 
#           target="image", 
#           process_type="single", 
#           mode="singular", 
#           augmentations=augmentations, 
#           aug_verbose=True)


# # Single Video Augmentation
# from CVAugmentor import Augmentations as aug
# from CVAugmentor import Pipeline


# ## Define the augmentations
# augmentations = {
#     "zoom": aug.Zoom(),
#     "flip": aug.Flip(),
# }

# ## Create a Pipeline object
# p = Pipeline()

# ## Augment the video
# p.augment(input_path="util_resources/samples/videos/0.mp4", 
#           output_path="util_resources/experiments/single_video/0.mp4", 
#           target="video", 
#           process_type="single", 
#           mode="sequential", 
#           augmentations=augmentations, 
#           aug_verbose=True)


# # Augmenting Multiple Images
# from CVAugmentor import Augmentations as aug
# from CVAugmentor import Pipeline


# ## Define the augmentations
# augmentations = {
#     "blur": aug.Blur(),
#     "brightness": aug.Brightness(),
#     "cutout": aug.Cutout(),
#     "expsure": aug.Exposure(),
#     "flip": aug.Flip(),
#     "grayscale": aug.Grayscale(),
#     "hue": aug.Hue(),
#     "negative": aug.Negative(),
#     "no_augmentation": aug.NoAugmentation(),
#     "noise": aug.Noise(),
#     "rotate": aug.Rotate(),
#     "saturation": aug.Saturation(),
#     "shear": aug.Shear(),
#     "zoom": aug.Zoom(),
# }

# ## Create a Pipeline object
# p = Pipeline()

# ## Augment the images
# p.augment(input_path="util_resources/samples/images", 
#           output_path="util_resources/experiments/multi_image", 
#           target="image", 
#           process_type="batch", 
#           mode="singular", 
#           augmentations=augmentations, 
#           verbose=True, 
#           warn_verbose=True,
#           random_state=True)


# Augmenting Multiple Videos
from CVAugmentor import Augmentations as aug
from CVAugmentor import Pipeline


## Define the augmentations
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

## Create a Pipeline object
p = Pipeline()

## Augment the videos
p.augment(input_path="util_resources/samples/videos", 
          output_path="util_resources/experiments/multi_video", 
          target="video", 
          process_type="batch", 
          mode="singular", 
          augmentations=augmentations, 
          verbose=True, 
          warn_verbose=True,
          random_state=True)