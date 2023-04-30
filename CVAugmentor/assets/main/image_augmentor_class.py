# Importing the libraries
from typing import Dict, Callable, Optional
from PIL import Image
import os


# Defining the ImageAugmentor class
class ImageAugmentor():
    
    def __init__(self) -> None:

        """

        Constructor of the ImageAugmentor class.
        
        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """
        
        pass


    def augment_one_by_one(self, image_path: str, output_path: str, augmentations: Dict[str, Callable], verbose: Optional[bool] = False) -> None:

        """

        Augments the image one augmentation at a time.
        This means that the image will be augmented by the first augmentation, then it will be saved. 
        Next the image will be augmented by the second augmentation, then it will be saved. And so on.

        
        Parameters
        ----------
        image_path : str
            Path to the image file to be augmented.
            
        output_path : str
            Path to the output image file.

        augmentations : dict
            Dict of augmentations to be applied to the image. 
            The keys are the names of the augmentations and the values are the augmentations themselves.

        verbose : bool, optional
            If True, prints the progress of the augmentation process. The default is False.

        
        Returns
        -------
        None.
        
        """

        # Applying the augmentations
        for name, augmentation in augmentations.items():

            # Loading the image
            image = Image.open(image_path)

            # Applying the augmentation
            image = augmentation(image)

            # Saving the augmented image
            image.save(os.path.splitext(output_path)[0] + '_' + name + os.path.splitext(image_path)[1])

            # Printing the progress
            if verbose:
                print('Applied the ' + name + ' augmentation.')


        # Print a message
        if verbose:
            print('Augmentation completed.')


    def augment_all_at_once(self, image_path: str, output_path: str, augmentations: Dict[str, Callable], verbose: Optional[bool] = False) -> None:

        """

        Augments the image all at once.
        This means that the image will be augmented by all the augmentations at once, then it will be saved.

        
        Parameters
        ----------
        image_path : str
            Path to the image file to be augmented.

        output_path : str
            Path to the output image file.

        augmentations : dict
            Dict of augmentations to be applied to the image. 
            The keys are the names of the augmentations and the values are the augmentations themselves.

        verbose : bool, optional
            If True, prints the progress of the augmentation process. The default is False.

        
        Returns
        -------
        None.
        
        """

        # Loading the image
        image = Image.open(image_path)

        # Applying the augmentations
        for _, augmentation in augmentations.items():

            # Applying the augmentation
            image = augmentation(image)

        # Saving the augmented image
        image.save(output_path)


        # Print a message
        if verbose:
            print('Augmentation completed.')