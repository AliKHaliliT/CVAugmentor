import logging
from typing import Optional, Union
from PIL import Image, ImageFilter
import numpy as np


# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


class Blur:

    """

    Apply a blur effect to an image.
    

    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self, radius: Optional[Union[int, float]] = None) -> None:

        """ 

        Constructor of the Blur class.

        
        Parameters
        ----------
        radius : int or float, optional
            Blur radius. The blur radius is the standard deviation of the Gaussian blur.
            The default value is `None`. If `None`, a random blur radius will be used.

            
        Returns
        -------
        None.
        
        """

        if radius is not None and not isinstance(radius, (int, float)):
            raise ValueError(f"radius must either be an int or a float. Received: {radius} with type {type(radius)}")
        
        if radius > 5:
            logging.warning("Radius should ideally be between 0 and 5.")
        

        self.radius = radius


    def _blur(self, image: Image.Image) -> Image.Image:

        """ 

        The blur operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        blurred_image : Image.Image
            The blurred image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")


        # Apply the Gaussian blur filter to the image and return it
        return image.filter(ImageFilter.GaussianBlur((self.radius or np.random.randint(0, 5))))


    def __call__(self, image: Image.Image) -> Image.Image:

        """ 

        Perform the blur operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        blurred_image : Image.Image
            The blurred image.

        """


        return self._blur(image)