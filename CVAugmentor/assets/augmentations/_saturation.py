from typing import Optional, Union
from PIL import Image, ImageEnhance
import numpy as np


class Saturation:

    """

    Adjust the saturation of an image. Saturation refers to the intensity or purity of the color.


    Usage
    -----
    The class instance must be called.

    """

    def __init__(self, saturation_factor: Optional[Union[int, float]] = None) -> None:

        """

        Constructor of the Saturation class.

        
        Parameters
        ----------
        saturation_factor : int or float, optional
            Saturation factor. If `None`, a random saturation factor will be used. The default value is `None`.

            
        Returns
        -------
        None.

        """

        if saturation_factor is not None and not isinstance(saturation_factor, (int, float)):
            raise ValueError(f"saturation_factor must either be an int or a float. Received: {saturation_factor} with type {type(saturation_factor)}")


        self.saturation_factor = saturation_factor


    def _saturation(self, image: Image.Image) -> Image.Image:

        """

        The saturation adjustment operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        img_saturated : Image.Image
            The saturation adjusted image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")
        

        # Convert the image to the HSV color space and enhance saturation
        return ImageEnhance.Color(image).enhance(1 + (self.saturation_factor or np.random.uniform(0, 0.5)))


    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the saturation adjustment operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        img_saturated : Image.Image
            The saturation adjusted image.

        """


        return self._saturation(image)