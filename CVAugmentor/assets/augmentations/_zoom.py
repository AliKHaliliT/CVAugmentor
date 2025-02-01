from typing import Optional, Union
from PIL import Image
import numpy as np


class Zoom:

    """

    Zoom an image by a specified or a random size.


    Usage
    -----
    The class instance must be called.

    """

    def __init__(self, zoom_size: Optional[tuple[Union[int, float], Union[int, float]]] = None) -> None:

        """

        Constructor of the Zoom class.

        
        Parameters
        ----------
        zoom_size : tuple, optional
            Size of the zoom as (width, height). The default value to `None`. If `None`, a random zoom size will be used.

            
        Returns
        -------
        None.

        """

        if zoom_size is not None and (not isinstance(zoom_size, tuple) or len(zoom_size) != 2 or any(x <= 0 for x in zoom_size)):
            raise ValueError(f"zoom_size must be a tuple of length two woth positive numbers. Received: {zoom_size} with type {type(zoom_size)}")
            

        self.zoom_size = zoom_size
        self.random_state = np.random.randint(1, 99)
        self.x = None
        self.y = None


    def _zoom(self, image: Image.Image) -> Image.Image:

        """

        The zoom operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.


        Returns
        -------
        zoomed_image : Image.Image
            The zoomed image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")
        

        if not self.zoom_size or not self.zoom_size.shape[::-1] == image.size:
            self.zoom_size = (
                                np.random.RandomState(self.random_state).randint(min(image.size[0], image.size[1]) // 2.5, min(image.size[0], image.size[1]) // 1.5),
                                np.random.RandomState(self.random_state).randint(min(image.size[0], image.size[1]) // 2.5, min(image.size[0], image.size[1]) // 1.5)
                             )

        if not self.x:
            self.x = np.random.RandomState(self.random_state).randint(0, image.size[0] - self.zoom_size[0])
            self.y = np.random.RandomState(self.random_state).randint(0, image.size[1] - self.zoom_size[1])

        
        return (image.crop((self.x, self.y, self.x + self.zoom_size[0], self.y + self.zoom_size[1]))).resize((image.size[0], image.size[1]))


    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the zoom operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.


        Returns
        -------
        zoomed_image : Image.Image
            The zoomed image.

        """


        return self._zoom(image)