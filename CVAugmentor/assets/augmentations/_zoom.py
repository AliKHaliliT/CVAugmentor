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

        if zoom_size is not None:
            if (not isinstance(zoom_size, tuple) or len(zoom_size) != 2 or not all(isinstance(v, (int, float)) and v >= 0 for v in zoom_size)):
                raise ValueError(f"zoom_size must be a tuple of length two with positive numbers. Received: {zoom_size} with type {type(zoom_size)}")
            

        self.zoom_size = zoom_size
        self.random_state = np.random.randint(1, 99)


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
        

        zoom_size = self.zoom_size if self.zoom_size is not None else (
            np.random.RandomState(self.random_state).randint(min(image.size[0], image.size[1]) // 2.5, min(image.size[0], image.size[1]) // 1.5),
            np.random.RandomState(self.random_state).randint(min(image.size[0], image.size[1]) // 2.5, min(image.size[0], image.size[1]) // 1.5)
        )

        x = np.random.RandomState(self.random_state).randint(0, image.size[0] - zoom_size[0])
        y = np.random.RandomState(self.random_state).randint(0, image.size[1] - zoom_size[1])

        
        return (image.crop((x, y, x + zoom_size[0], y + zoom_size[1]))).resize((image.size[0], image.size[1]))


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