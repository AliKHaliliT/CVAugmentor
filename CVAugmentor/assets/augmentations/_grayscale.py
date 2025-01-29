from PIL import Image


class Grayscale:

    """

    Convert an image to grayscale.
    The image remains in RGB format for consistency with other methods.


    Usage
    -----
    The class instance must be called.

    """

    def __init__(self) -> None:

        """

        Constructor of the Grayscale class.

        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.

        """

        pass


    def _grayscale(self, image: Image.Image) -> Image.Image:

        """

        The grayscale conversion operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        grayscaled_image : Image.Image
            The grayscaled image in RGB format.

        """

        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of the PIL Image")


        # Create a new image with 3 channels by copying the grayscale image (created using the RGB weighted method)
        return Image.merge("RGB", (image.convert("L"),) * 3)
    

    def __call__(self, image: Image.Image) -> Image.Image:

        """

        Perform the grayscale conversion operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.

            
        Returns
        -------
        grayscaled_image : Image.Image
            The grayscaled image in RGB format.

        """


        return self._grayscale(image)