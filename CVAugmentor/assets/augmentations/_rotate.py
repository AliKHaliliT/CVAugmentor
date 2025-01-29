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

    def __init__(self, rotate_type: str = "definite", 
                 angle: Union[int, float] = 90) -> None:

        """

        Constructor of the Rotate class.

        
        Parameters
        ----------
        rotate_type : str, optional
            Type of rotation. The default value is `"definite"`.
                The options are:
                    `"definite"`
                        Rotate the image by a fixed angle.
                    `"random"`
                        Rotate the image by a random angle.

        angle : int or float, optional
            Angle of rotation. The default value is `90`.

            
        Returns
        -------
        None.

        """

        if rotate_type not in ["definite", "random"]:
            raise ValueError("rotate_type must either be 'definite' or 'random'")
        if not isinstance(angle, (int, float)):
            raise ValueError("angle must be an integer or float")


        self.rotate_type = rotate_type
        self.angle = angle


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
            raise TypeError("image must be an instance of the PIL Image")


        return image.rotate((self.angle or np.random.randint(-self.angle, self.angle)))


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