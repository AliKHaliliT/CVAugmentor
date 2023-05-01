# Importing the libraries
from .assets.utils.alphanumeric_sorter_class import AlphanumericSorter
from .assets.utils.file_type_checker_class import FileTypeChecker
from .assets.main.video_augmentor_class import VideoAugmentor
from .assets.main.image_augmentor_class import ImageAugmentor
from typing import Dict, Callable, Optional
import os
from tqdm import tqdm


# Defining the Pipeline class
class Pipeline(AlphanumericSorter, FileTypeChecker):

    # Defining the constructor
    def __init__(self) -> None:

        """

        Constructor of the Pipeline class.
        Initializes the AlphanumericSorter, ImageAugmentor and VideoAugmentor classes.

        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    # Defining the augment method
    def augment(self, input_path: str, output_path: str, target: str, process_type: str, mode: str,
                augmentations: Dict[str, Callable], verbose: Optional[bool] = False, aug_verbose: Optional[bool] = False, warn_verbose: Optional[bool] = False) -> None:
        
        """
        
        Augments the input data.


        Parameters
        ----------
        input_path : str
            Path to the input data.

        output_path : str
            Path to the output data.

        target : str
            Target of the augmentation.
                The options are:
                    "image"
                        Specifies that the target of the augmentation is an image.
                    "video"
                        Specifies that the target of the augmentation is a video.

        process_type : str
            Type of the augmentation.
                The options are:
                    "batch"
                        Batch type means that the input and output paths are directories.
                    "single"
                        Single type means that the input and output paths are files.

        mode : str
            Mode of the augmentation.
                The options are:
                    "sequential"
                        Sequential mode means that the augmentations will be applied one by one.
                        This means that the data will be saved after each augmentation.
                    "singular"
                        Singular mode means that the augmentations will be applied all at once.
                        This means that the data will be saved only after all augmentations were applied.

        augmentations : dict
            Dict of augmentations to be applied to the data. 
            The keys are the names of the augmentations and the values are the augmentations themselves.

        verbose : bool, optional
            If True, prints the progress of the augmentation process. The default is False.

        
        Returns
        -------
        None.
        
        """

        # Checking if the input path is valid
        if not os.path.exists(input_path):
            raise ValueError(f"Invalid input path: {input_path}")
        
        # Checking if the process_type is valid
        if process_type != "batch" and process_type != "single":
            raise ValueError(f"Invalid process type: {process_type}")
        
        # Checking if the output path is valid
        if process_type == "batch" and not os.path.exists(output_path):
            raise ValueError(f"Invalid output path: {output_path}")

        # Checking if the target is valid
        if target != "image" and target != "video":
            raise ValueError(f"Invalid target type: {target}")
        
        # Checking if the mode is valid
        if mode != "sequential" and mode != "singular":
            raise ValueError(f"Invalid mode type: {mode}")
        
        # Checking if the augmentations is valid
        if not isinstance(augmentations, dict):
            raise ValueError(f"Invalid augmentations type: {process_type}")
        elif len(augmentations) == 0:
            raise ValueError("augmentations dict is empty.")
        
        # Checking if the verbose is valid
        if not isinstance(verbose, bool):
            raise ValueError(f"Invalid verbose type: {verbose}")


        # Choosing the augmentor
        if target == "image":
            augmentor = ImageAugmentor()
        elif target == "video":
            augmentor = VideoAugmentor()
        else:
            raise ValueError(f"Invalid target type: {target}")
        
        # Augmentation
        if process_type == "batch":
            
            # Looping through the input files
            for input_file in tqdm(self.sorted_alphanumeric(os.listdir(input_path)), desc='Overall Progress', unit=' Videos', leave=False, dynamic_ncols=True, diable=not verbose):
                
                # Checking if the input file is valid
                if not self.is_target_type(input_file, target):

                    if warn_verbose:
                        print(f"Skipping invalid input file: {input_file}")

                    continue

                # Defining the input file path
                input_file_path = os.path.join(input_path, input_file)

                # Defining the output file path
                output_file_path = os.path.join(output_path, input_file)

                # Augmenting the input file
                if mode == "sequential":
                    augmentor.augment_one_by_one(input_file_path, output_file_path, augmentations, aug_verbose)
                elif mode == "singular":
                    augmentor.augment_all_at_once(input_file_path, output_file_path, augmentations, aug_verbose)

        elif process_type == "single":
                
                # Checking if the input file is valid
                if not self.is_target_type(input_path, target):
                    raise ValueError(f"Invalid input file. Expected {target} file, got {os.path.splitext(input_path)[1]} instead.")
                
                # Checking if the format of the input file and the output file are the same
                if os.path.splitext(input_path)[1] != os.path.splitext(output_path)[1]:
                    raise ValueError(f"Input file format and output file format are not the same. Got {os.path.splitext(input_path)[1]} in input, and {os.path.splitext(output_path)[1]} in output.")
                elif os.path.splitext(input_path)[1] == ".gif":
                    raise ValueError(f"The GIF format is not supported.")
                
                # Augmenting the input file
                if mode == "sequential":
                    augmentor.augment_one_by_one(input_path, output_path, augmentations, verbose)
                elif mode == "singular":
                    augmentor.augment_all_at_once(input_path, output_path, augmentations, verbose)