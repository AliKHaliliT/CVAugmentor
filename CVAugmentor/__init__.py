"""

The CVAugmentor Augmentation Package.


CVAugmentor is a Python package designed for augmenting images and videos, making it easier to enhance and modify visual data for computer vision tasks. 
It provides a collection of utilities that automate transformations such as flipping, rotation, scaling, color adjustments, and more. 

"""
from .assets.main.pipeline import Pipeline
from .assets import augmentations as Augmentations


__version__ = "1.1.2"