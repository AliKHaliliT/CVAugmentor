import logging
from typing import Optional, Union
from PIL import Image
import numpy as np


# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


class Shear:

    """

    Shear an image along the x-axis and/or y-axis. The shearing means that the image is slanted along the axis.


    Usage
    -----
    The class instance must be called.

    """

    def __init__(self, shear: Optional[tuple[Union[int, float], Union[int, float]]] = None) -> None:

        """

        Constructor of the Shear class.
        

        Parameters
        ----------
        shear : tuple, optional
            Shear values for x and y axes. The default value is `None`.
            If `None`, random shear values are generated.
            

        Returns
        -------
        None.

        """

        if shear is not None and (not isinstance(shear, tuple) or len(shear) != 2) and not (-1 <= shear[0] <= 1 and -1 <= shear[1] <= 1):
            raise ValueError("shear must be a tuple of decimal values (x, y) between -1 and 1")

        if not (-0.5 <= shear[0] <= 0.5 and -0.5 <= shear[1] <= 0.5):
            logging.warning("The optimal value for shear is between -0.5 and 0.5.")


        self.shear = shear


    def _shear(self, image: Image.Image) -> Image.Image:

        """

        The shearing operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        sheared_image : Image.Image
            The sheared image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of the PIL Image")
        

        shear = self.shear or (np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5))


        return image.transform(image.size, Image.AFFINE, (1, shear[0], 0, shear[1], 1, 0))


    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the shearing operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        sheared_image : Image.Image
            The sheared image.

        """


        return self._shear(image)