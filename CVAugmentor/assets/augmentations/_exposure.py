import logging
from typing import Optional, Union
from PIL import Image
import numpy as np


# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


class Exposure:

    """

    Adjust the exposure of an image. The exposure means the amount of light that reaches the image sensor.


    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self, exposure_factor: Optional[Union[int, float]] = None) -> None:

        """ 

        Constructor of the Exposure class.

        
        Parameters
        ----------
        exposure_factor : int or float, optional
            Exposure factor. The default value is `None`. If `None`, a random exposure factor will be used.

            
        Returns
        -------
        None.
        
        """

        if exposure_factor is not None and not isinstance(exposure_factor, (int, float)):
            raise ValueError("exposure_factor must either be an int or a float")
        
        if not 0.3 <= exposure_factor <= 1.7:
            logging.warning("Exposure factor should ideally be between 0.3 and 1.7.")
        

        self.exposure_factor = exposure_factor


    def _expose(self, image: Image.Image) -> Image.Image:

        """ 

        The exposure adjustment operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        exposed_image : Image.Image
            The exposure adjusted image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of the PIL Image")


        return Image.fromarray(np.clip((np.array(image) * (self.exposure_factor or np.random.uniform(0.3, 1.7))), 0, 255).astype(np.uint8))


    def __call__(self, image: Image.Image) -> Image.Image:

        """ 

        Perform the exposure adjustment operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        exposed_image : Image.Image
            The exposure adjusted image.

        """


        return self._expose(image)