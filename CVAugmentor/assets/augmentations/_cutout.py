from typing import Optional, Union
from PIL import Image
import numpy as np


class Cutout:

    """

    Cutout a random part of the image. This operation cuts out a random part of the image and replaces it with a black rectangle.


    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self, max_count: Optional[int] = None, 
                 max_size: Optional[Union[int, float]] = None) -> None:

        """ 

        Constructor of the Cutout class.

        
        Parameters
        ----------
        max_count : int, optional
            Maximum number of cutouts. The default value is `None`. If `None`, a random maximum count will be used.
        
        max_size : int or float, optional
            Maximum size of the cutout. The default value is `None`. If `None`, a random maximum size will be used.
            

        Returns
        -------
        None.
        
        """

        if max_count is not None and not isinstance(max_count, int):
            raise ValueError("max_count must be an integer")
        if max_size is not None and not isinstance(max_size, (int, float)):
            raise ValueError("max_size must either be an int or a float")
        

        self.max_count = max_count
        self.max_size = max_size


    def _cutout(self, image: Image.Image) -> Image.Image:

        """ 

        The cutout operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        cutout_image : Image.Image
            The cutout image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of the PIL Image")
        

        max_size = self.max_size or np.random.randint(1, min(image.size[0], image.size[1]) // 4)

        img_array = np.array(image)

        for _ in range((self.max_count or np.random.randint(1, 6))):
            y = np.random.randint(0, image.size[0] - max_size + 1)
            x = np.random.randint(0, image.size[1] - max_size + 1)
            img_array[x:x + max_size, y:y + max_size, :] = 0


        return Image.fromarray(img_array)


    def __call__(self, image: Image.Image) -> Image.Image:

        """ 

        Perform the cutout operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        cutout_image : Image.Image
            The cutout image.

        """


        return self._cutout(image)