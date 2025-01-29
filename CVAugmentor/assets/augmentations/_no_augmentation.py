from PIL import Image


class NoAugmentation:

    """
    
    No augmentation. 
    This can be used when you want to copy the image to the output folder without augmenting it.


    Usage
    -----
    The class instance must be called.
    
    """

    def __init__(self) -> None:
        
        """

        Constructor of the No Augmentation class.
        
        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    def _no_augmentation(self, image: Image.Image) -> Image.Image:
            
        """

        The no augmentation operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.


        Returns
        -------
        image : Image.Image
            The original image.

        """

        if not isinstance(image, Image.Image):
            raise TypeError("image must be an instance of the PIL Image")
        

        return image
    

    def __call__(self, image: Image.Image) -> Image.Image:
            
        """

        Perform the no augmentation operation.

        
        Parameters
        ----------
        image : Image.Image
            The image to be augmented.


        Returns
        -------
        image : Image.Image
            The original image.

        """


        return self._no_augmentation(image)