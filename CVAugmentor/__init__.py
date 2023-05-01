"""

The CVAugmentor Augmentation Package.


CVAugmentor is a python package for augmenting image and video files. It provides a number of utilities that aid augmentation \
in a automated manner. The aim of the package is to make augmentation easier.
The package is built on top of the OpenCV and Pillow libraries.

"""
# Importing the libraries
from .pipeline import Pipeline
from .assets.main.augmentations_class import Augmentations


# Defining the version
__version__ = '1.0.9'