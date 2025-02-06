from typing import Union
from ...image_augmentor import ImageAugmentor
from ...video_augmentor import VideoAugmentor


def _choose_augmentor(target: str) -> Union[ImageAugmentor, VideoAugmentor]:

    """
    
    Returns the target augmentor.


    Parameters
    ----------
    target : str
        Target of the augmentation.
            The options are:
                "image"
                    Specifies that the target of the augmentation is an image.
                "video"
                    Specifies that the target of the augmentation is a video.

    Returns
    -------
    None.
    
    """

    if target == "image":
        return ImageAugmentor()
    elif target == "video":
        return VideoAugmentor()