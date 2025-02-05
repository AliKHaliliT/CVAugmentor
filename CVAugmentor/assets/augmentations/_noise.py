import logging
from typing import Optional, Union
from PIL import Image
import numpy as np


# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")


class Noise:

    """

    Add noise to the image. This method adds noise to the image by multiplying the pixel values by a random number between -1 and 1.
    It creates a noisy image that looks like the output from an analog TV with bad reception.


    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self, intensity: Optional[Union[int, float]] = None) -> None:

        """ 

        Constructor of the Noise class.

        
        Parameters
        ----------
        intensity : int or float, optional
            Noise intensity. The default value is `None`. If `None`, a random noise intensity will be used.

            
        Returns
        -------
        None.
        
        """

        if intensity is not None and not isinstance(intensity, (int, float)):
            raise ValueError(f"intensity must either be an int or a float. Received: {intensity} with type {type(intensity)}")
        

        self.noise = None
        self.random_state = np.random.randint(1, 99)
        self.intensity = intensity if intensity is not None else np.random.uniform(-1, 1)

        if not -1 <= self.intensity <= 1:
            logging.warning("The optimal value for intensity is between -1 and 1.")


    def _noise(self, image: Image.Image) -> Image.Image:

        """ 

        The noise operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        noised_image : Image.Image
            The noised image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")


        # Convert the image to a numpy array
        img_array = np.array(image)
        
        # Generate a noise array with the same dimensions as the image
        if self.noise is not None:
            if not self.noise.shape == img_array.shape:
                self.noise = np.random.RandomState(self.random_state).rand(*img_array.shape) * self.intensity
        else:
            self.noise = np.random.RandomState(self.random_state).rand(*img_array.shape) * self.intensity
        
        # Add the noise to the pixel values of the image
        noised_image = np.clip(img_array + self.noise * 255, 0, 255).astype(np.uint8)


        return Image.fromarray(noised_image)


    def __call__(self, image: Image.Image) -> Image.Image:

        """ 

        Perform the noise operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        noised_image : Image.Image
            The noised image.

        """


        return self._noise(image)