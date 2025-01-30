from typing import Union, Callable
from ...image_augmentor import ImageAugmentor
from ...video_augmentor import VideoAugmentor
from tqdm import tqdm
from ....utils.sort_alphanumerically import sorted_alphanumerically
from ....utils.file_type_checker import is_target_type
import os
from ._apply_augmentations import _apply_augmentation


def _process_batch(input_path: str, 
                   verbose: bool,
                   target: str,
                   warn_verbose: bool,
                   output_path: str, 
                   mode: str,
                   augmentor: Union[ImageAugmentor, VideoAugmentor],
                   augmentations: dict[str, Callable[..., None]], 
                   aug_verbose: bool) -> None:
    
    """
    
    Processes the input directory.


    Parameters
    ----------
    input_path : str
        Path to the input data.

    verbose : bool, optional
        If True, prints the overall progress of the augmentation process. The default value is `False`.

    target : str
        Target of the augmentation.
            The options are:
                "image"
                    Specifies that the target of the augmentation is an image.
                "video"
                    Specifies that the target of the augmentation is a video.

    warn_verbose : bool, optional
        If True, prints the warnings. The default value is `False`.

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

    
    Returns
    -------
    None.
    
    """

    for input_file in tqdm(total=sorted_alphanumerically(os.listdir(input_path)), 
                            desc="Overall progress", 
                            unit="videos", 
                            ncols=100,
                            unit_scale=True,
                            dynamic_ncols=True,
                            disable=not verbose):
        
        if not is_target_type(input_file, target):
            if warn_verbose:
                print(f"Skipping invalid input file: {input_file}")
            continue

        input_file_path = os.path.join(input_path, input_file)
        output_file_path = os.path.join(output_path, input_file)


        _apply_augmentation(mode, augmentor, input_file_path, output_file_path, augmentations, aug_verbose)