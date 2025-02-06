from PIL import Image, ImageOps


class Negative:

    """

    Convert the image to negative. This operation converts the image to negative by inverting its pixel values.

    
    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self) -> None:

        """ 

        Constructor of the Negative class.
        
        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    def _negative(self, image: Image.Image) -> Image.Image:

        """ 

        The negative operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        negative_image : Image.Image
            The negative image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError(f"image must be an instance of the PIL Image. Received: {image} with type {type(image)}")


        # Convert the image to negative by inverting the pixel values
        return ImageOps.invert(image.convert("RGB"))


    def __call__(self, image: Image.Image) -> Image.Image:

        """ 

        Perform the negative operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        negative_image : Image.Image
            The negative image.

        """


        return self._negative(image)