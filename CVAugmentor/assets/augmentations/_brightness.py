from typing import Optional, Union
from PIL import Image, ImageEnhance
import numpy as np


class Brightness:

    """

    Adjust the brightness of an image.
    

    Usage
    -----
    The class instance must be called.

    """

    def __init__(self, brightness_factor: Optional[Union[int, float]] = None) -> None:

        """

        Constructor of the Brightness class.

        
        Parameters
        ----------
        brightness_factor : int or float, optional
            Brightness factor. The default value is `None`. If `None`, a random brightness factor will be used.

            
        Returns
        -------
        None.

        """

        if brightness_factor is not None and not isinstance(brightness_factor, (int, float)):
            raise ValueError("brightness_factor must either be an int or a float")


        self.brightness_factor = brightness_factor


    def _brightness(self, image: Image.Image) -> Image.Image:

        """

        The brightness adjustment operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        img_brightened : Image.Image
            The brightness adjusted image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of the PIL Image")

        
        return ImageEnhance.Brightness(image).enhance(1 + (self.brightness_factor or np.random.uniform(0, 0.5)))


    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the brightness adjustment operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        img_brightened : Image.Image
            The brightness adjusted image.

        """


        return self._brightness(image)