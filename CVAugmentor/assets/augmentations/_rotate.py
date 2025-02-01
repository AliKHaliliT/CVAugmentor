from typing import Union
from PIL import Image
import numpy as np


class Rotate:

    """

    Rotate an image by a definite or random angle.


    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self, angle: Union[int, float] = 90) -> None:

        """

        Constructor of the Rotate class.

        
        Parameters
        ----------
        angle : int or float, optional
            Angle of rotation. The default value is `90`.

            
        Returns
        -------
        None.

        """

        if not isinstance(angle, (int, float)):
            raise ValueError(f"angle must be an integer or float. Received: {angle} with type {type(angle)}")
        

        self.angle = angle or np.random.randint(-self.angle, self.angle)


    def _rotate(self, image: Image.Image) -> Image.Image:

        """

        The rotation operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        rotated_image : Image.Image
            The rotated image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")


        return image.rotate(self.angle)


    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the rotation operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        rotated_image : Image.Image
            The rotated image.

        """


        return self._rotate(image)