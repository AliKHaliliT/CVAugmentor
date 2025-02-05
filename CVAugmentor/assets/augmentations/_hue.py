from typing import Optional, Union
from PIL import Image
import numpy as np


class Hue:

    """

    Shift the hue of an image by a specified or random value.

    
    Usage
    -----
    The class instance must be called.

    """

    def __init__(self, hue_shift: Optional[Union[int, float]] = None) -> None:

        """
        
        Constructor of the Hue class.

        
        Parameters
        ----------
        hue_shift : int or float, optional
            Hue shift value. The default value is `None`. If `None`, a random hue shift value will be used.
            

        Returns
        -------
        None.

        """

        if hue_shift is not None:
            if not isinstance(hue_shift, (int, float)) or (hue_shift < -360 or hue_shift > 360):
                raise ValueError(f"hue_shift must either be an int or a float between -360 and 360. Received: {hue_shift} with type {type(hue_shift)}")
        

        self.hue_shift = hue_shift if hue_shift is not None else np.random.uniform(-360, 360)


    def _hue(self, image: Image.Image) -> Image.Image:

        """
        
        The hue shift operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.
            

        Returns
        -------
        img_hued : Image.Image
            The hue-shifted image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")
        
        import warnings
        warnings.warn(f"{self.hue_shift}")
        

        h, s, v = image.convert("HSV").split()

        h_data = (np.array(h) + self.hue_shift) % 256
        h = Image.fromarray(h_data.astype("uint8"), mode='L')


        return Image.merge("HSV", (h, s, v)).convert("RGB")


    def __call__(self, image: Image.Image) -> Image.Image:

        """
        
        Perform the hue shift operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.
            

        Returns
        -------
        img_hued : Image.Image
            The hue-shifted image.

        """
        

        return self._hue(image)