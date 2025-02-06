from typing import Union, Callable
from ...image_augmentor import ImageAugmentor
from ...video_augmentor import VideoAugmentor


def _apply_augmentation(mode: str, 
                        augmentor: Union[ImageAugmentor, VideoAugmentor], 
                        input_file_path: str, 
                        output_file_path: str, 
                        augmentations: dict[str, Callable[..., None]], 
                        aug_verbose: bool,
                        target: str,
                        process_type: str) -> None:
    
    """
    
    Applies the augmentation.


    Parameters
    ----------
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

    input_file_path : str
        Path to the input data.

    output_file_path : str
        Path to the output data.

    augmentations : dict
        A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

    aug_verbose : bool, optional
        If True, prints the progress of the augmentation process. The default value is `False`.

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
                "single"
                    Single type means that the input and output paths are files.
                "batch"
                    Batch type means that the input and output paths are directories.

    
    Returns
    -------
    None.
    
    """
                        
    if mode == "sequential":
        augmentor.apply_sequentially(input_file_path, output_file_path, augmentations, aug_verbose)
    elif mode == "singular":
        if target == "image":
            augmentor.apply_in_batch(input_file_path, output_file_path, augmentations, aug_verbose)
        elif target == "video":
            if process_type == "single":
                augmentor.apply_in_batch(input_file_path, output_file_path, augmentations, aug_verbose)
            elif process_type == "batch":
                augmentor.apply_in_batch(input_file_path, output_file_path, augmentations, aug_verbose, leave=True)