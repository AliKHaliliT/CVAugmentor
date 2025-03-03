from typing import Callable, Optional
from tqdm import tqdm
from PIL import Image
import os


class ImageAugmentor():

    """

    This class applies a series of image augmentations and saves the results.
    It processes an input image using a set of augmentation functions, either sequentially or in a batch. 
    Augmentations are provided as a dictionary, where keys are names and values are callable functions.

    """
    
    def __init__(self) -> None:

        """

        Constructor of the Image Augmentor class.


        Parameters
        ----------
        None.

            
        Returns
        -------
        None.

        """


    def _validate_inputs(self, image_path, output_path, augmentations, verbose):

        """

        Validates input parameters.


        Parameters
        ----------
        image_path : str
            Path to the input image file.

        output_path : str
            Path where the augmented image will be saved.

        augmentations : dict
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            Whether to display progress during the process. The default value is `False`.

            
        Returns
        -------
        None.

        """
        
        if not isinstance(image_path, str) or not os.path.isfile(image_path):
            raise ValueError(f"image_path must be a valid file path. Received: {image_path} with type {type(image_path)}")
        if not isinstance(output_path, str) or not os.path.isdir(os.path.dirname(output_path)):
            raise ValueError(f"output_path must be a valid directory path. Received: {output_path} with type {type(output_path)}")
        if not isinstance(augmentations, dict) or not all(isinstance(k, str) and callable(v) for k, v in augmentations.items()):
            raise ValueError(f"augmentations must be a dictionary with string keys and callable values. Received: {augmentations} with type {type(augmentations)}")
        if verbose is not None and not isinstance(verbose, bool):
            raise TypeError(f"verbose must be a boolean. Received: {verbose} with type {type(verbose)}")


    def apply_sequentially(self, 
                           image_path: str, 
                           output_path: str, 
                           augmentations: dict[str, Callable], 
                           verbose: Optional[bool] = False) -> None:

        """

        Applies each augmentation separately and saves individual results at each augmentation.

        
        Parameters
        ----------
        image_path : str
            Path to the input image file.

        output_path : str
            Path where the augmented image will be saved.

        augmentations : dict
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            Whether to display progress during the process. The default value is `False`.

            
        Returns
        -------
        None.

        """

        self._validate_inputs(image_path, output_path, augmentations, verbose)


        # Applying the augmentation
        for name, augmentation in tqdm(iterable=augmentations.items(),
                                       desc="Applying augmentation" if len(augmentations.items()) == 1 else "Applying augmentations",
                                       unit="augmentation" if len(augmentations.items()) == 1 else "augmentations",
                                       dynamic_ncols=True,
                                       disable=not verbose):
            
            augmentation(Image.open(image_path)).save(
                f"{os.path.splitext(output_path)[0]}_{name}{os.path.splitext(output_path)[1]}"
            )


    def apply_in_batch(self, 
                       image_path: str, 
                       output_path: str, 
                       augmentations: dict[str, Callable], 
                       verbose: Optional[bool] = False) -> None:

        """

        Applies all augmentations in sequence to the same image and saves the final output.

        
        Parameters
        ----------
        image_path : str
            Path to the input image file.

        output_path : str
            Path where the augmented image will be saved.

        augmentations : dict
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            Whether to display progress during the process. The default value is `False`.

            
        Returns
        -------
        None.

        """

        self._validate_inputs(image_path, output_path, augmentations, verbose)

        image = Image.open(image_path)

        # Applying the augmentations
        for augmentation in tqdm(iterable=augmentations.values(),
                                 desc="Applying augmentation" if len(augmentations.items()) == 1 else "Applying augmentations",
                                 unit="augmentation" if len(augmentations.items()) == 1 else "augmentations",
                                 dynamic_ncols=True,
                                 disable=not verbose):
            
            image = augmentation(image)

        image.save(output_path)