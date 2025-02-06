from typing import Union, Callable
from ...image_augmentor import ImageAugmentor
from ...video_augmentor import VideoAugmentor
from ....utils.file_type_checker import is_target_type
import os
from ._apply_augmentations import _apply_augmentation


def _process_single(input_path: str, 
                    target: str, 
                    output_path: str, 
                    mode: str, 
                    augmentor: Union[ImageAugmentor, VideoAugmentor], 
                    augmentations: dict[str, Callable[..., None]], 
                    aug_verbose: bool,
                    process_type: str) -> None:
    
    """
    
    Processes the input file.


    Parameters
    ----------
    input_path : str
        Path to the input data.

    target : str
        Target of the augmentation.
            The options are:
                "image"
                    Specifies that the target of the augmentation is an image.
                "video"
                    Specifies that the target of the augmentation is a video.

    output_path : str
        Path to the output data.

    mode : str
        Mode of the augmentation.
            The options are:
                "sequential"
                    Sequential mode means that the augmentations will be applied one by one.
                    This means that the data will be saved after each augmentation.
                "singular"
                    Singular mode means that the augmentations will be applied all at once.
                    This means that the data will be saved only after all augmentations were applied.

    augmentor : ImageAugmentor or VideoAugmentor
        The augmentor class.

    augmentations : dict
        A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

    aug_verbose : bool, optional
        If True, prints the progress of the augmentation process. The default value is `False`.

    process_type : str
        Type of the augmentation.
            The options are:
                "single"
                    Single type means that the input and output paths are files.
                "batch"
                    Batch type means that the input and output paths are directories.

    
    Returns
    -------
    None.
    
    """ 

    if not is_target_type(input_path, target):
        raise ValueError(f"Invalid input file. Expected {target} file, got {os.path.splitext(input_path)[1]} instead.")
    if os.path.splitext(input_path)[1] != os.path.splitext(output_path)[1]:
        raise ValueError(f"Input file format and output file format are not the same. Got {os.path.splitext(input_path)[1]} in input, and {os.path.splitext(output_path)[1]} in output.")
    elif os.path.splitext(input_path)[1] == ".gif":
        raise ValueError(f"The GIF format is not supported.")
    
    
    _apply_augmentation(mode, augmentor, input_path, output_path, augmentations, aug_verbose, target, process_type)