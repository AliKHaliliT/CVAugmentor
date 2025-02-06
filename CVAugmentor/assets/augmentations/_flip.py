from PIL import Image
import numpy as np


class Flip:

    """

    Flip the image horizontally or vertically.


    Usage
    -----
    The class instance must be called.

    """

    def __init__(self, flip_type: str = "vertical") -> None:

        """

        Constructor of the Flip class.

        
        Parameters
        ----------
        flip_type : str, optional
            Type of flip. The default value is `"vertical"`.
                The options are:
                    `"horizontal"`
                        Flip the image horizontally.
                    `"vertical"`
                        Flip the image vertically.

        Returns
        -------
        None.

        """

        if flip_type not in ["horizontal", "vertical"]:
            raise ValueError(f"flip_type must either be 'horizontal' or 'vertical'. Received: {flip_type} with type {type(flip_type)}")


        self.flip_type = flip_type


    def _flip(self, image: Image.Image) -> Image.Image:

        """

        The flip operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

        
        Returns
        -------
        flipped_image : Image
            The flipped image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")
        

        img = np.array(image)

        if self.flip_type == "horizontal":
            img = np.fliplr(img)
        elif self.flip_type == "vertical":
            img = np.flipud(img)


        return Image.fromarray(img)
    

    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the flip operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

        
        Returns
        -------
        flipped_image : Image
            The flipped image.

        """


        return self._flip(image)