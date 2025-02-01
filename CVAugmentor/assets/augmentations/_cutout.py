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

    def __init__(self, 
                 max_size: Optional[Union[int, float]] = None,
                 max_count: Optional[int] = None) -> None:

        """ 

        Constructor of the Cutout class.

        
        Parameters
        ----------
        max_size : int or float, optional
            Maximum size of the cutout. The default value is `None`. If `None`, a random maximum size will be used.

        max_count : int, optional
            Maximum number of cutouts. The default value is `None`. If `None`, a random maximum count will be used.
            

        Returns
        -------
        None.
        
        """

        if max_size is not None and not isinstance(max_size, (int, float)):
            raise ValueError(f"max_size must either be an int or a float. Received: {max_size} with type {type(max_size)}")
        if max_count is not None and not isinstance(max_count, int):
            raise ValueError(f"max_count must be an integer. Received: {max_count} with type {type(max_count)}")
        

        self.max_count = max_count or np.random.randint(1, 6)
        self.max_size = max_size
        self.random_state = np.random.randint(1, 99)


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
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")
        

        self.max_size = self.max_size or np.random.RandomState(self.random_state).randint(1, min(image.size[0], image.size[1]) // 4)

        img_array = np.array(image)

        for _ in range(self.max_count):
            y = np.random.RandomState(self.random_state).randint(0, image.size[0] - self.max_size + 1)
            x = np.random.RandomState(self.random_state).randint(0, image.size[1] - self.max_size + 1)
            img_array[x:x + self.max_size, y:y + self.max_size, :] = 0


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