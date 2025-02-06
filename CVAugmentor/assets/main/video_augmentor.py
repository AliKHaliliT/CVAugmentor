from typing import Callable, Optional
import cv2
from tqdm import tqdm
import os
import numpy as np
from PIL import Image


class VideoAugmentor():

    """

    This class applies a series of video augmentations and saves the results.
    It processes an input video using a set of augmentation functions, either sequentially or in a batch. 
    Augmentations are provided as a dictionary, where keys are names and values are callable functions.

    
    Methods
    -------
    apply_sequentially()
        Applies each augmentation separately and saves individual results.
        
    apply_in_batch()
        Applies all augmentations in sequence to the same video and saves the final output.

    """

    def __init__(self) -> None:

        """

        Constructor of the Video Augmentor class.


        Parameters
        ----------
        None.

            
        Returns
        -------
        None.

        """


    def _validate_inputs(self, video_path, output_path, augmentations, verbose):

        """

        Validates input parameters.


        Parameters
        ----------
        video_path : str
            Path to the input video file.

        output_path : str
            Path where the augmented video will be saved.

        augmentations : dict
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            Whether to display progress during the process. The default value is `False`.

            
        Returns
        -------
        None.

        """

        if not isinstance(video_path, str) or not os.path.isfile(video_path):
            raise ValueError(f"video_path must be a valid file path. Received: {video_path} with type {type(video_path)}")
        if not isinstance(output_path, str) or not os.path.isdir(os.path.dirname(output_path)):
            raise ValueError(f"output_path must be a valid directory path. Received: {output_path} with type {type(output_path)}")
        if not isinstance(augmentations, dict) or not all(isinstance(k, str) and callable(v) for k, v in augmentations.items()):
            raise ValueError(f"augmentations must be a dictionary with string keys and callable values. Received: {augmentations} with type {type(augmentations)}")
        if verbose is not None and not isinstance(verbose, bool):
            raise TypeError(f"verbose must be a boolean. Received: {verbose} with type {type(verbose)}")


    def apply_sequentially(self, 
                           video_path: str, 
                           output_path: str, 
                           augmentations: dict[str, Callable], 
                           verbose: Optional[bool] = False) -> None:
            
        """

        Applies each augmentation separately and saves individual results at each augmentation.

        
        Parameters
        ----------
        video_path : str
            Path to the input video file.

        output_path : str
            Path where the augmented video will be saved.

        augmentations : dict
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            Whether to display progress during the process. The default value is `False`.

            
        Returns
        -------
        None.

        """

        self._validate_inputs(video_path, output_path, augmentations, verbose)


        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))


        for name, augmentation in tqdm(iterable=augmentations.items(), 
                                       desc="Applying augmentations", 
                                       unit="augmentation", 
                                       ncols=100,
                                       dynamic_ncols=True,
                                       disable=not verbose):

            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            writer = cv2.VideoWriter(f"{os.path.splitext(output_path)[0]}_{name}{os.path.splitext(output_path)[1]}", 
                                     cv2.VideoWriter_fourcc(*"mp4v"), 
                                     (int(video.get(cv2.CAP_PROP_FPS))), 
                                     (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                                    )

            for _ in range(total_frames):
                ret, frame = video.read()
                if not ret:
                    break

                augmented_frame = np.array(augmentation(Image.fromarray(frame)))
                writer.write(augmented_frame)


            writer.release()

        video.release()


        if verbose:
            print("Augmentation complete.")


    # Defining the augment method
    def apply_in_batch(self, 
                       video_path: str, 
                       output_path: str, 
                       augmentations: dict[str, Callable], 
                       verbose: Optional[bool] = False) -> None:
        
        """

        Applies all augmentations in sequence to the same video and saves the final output.

        
        Parameters
        ----------
        video_path : str
            Path to the input video file.

        output_path : str
            Path where the augmented video will be saved.

        augmentations : dict
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            Whether to display progress during the process. The default value is `False`.

            
        Returns
        -------
        None.

        """

        self._validate_inputs(video_path, output_path, augmentations, verbose)
        

        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        writer = cv2.VideoWriter(
            output_path, 
            cv2.VideoWriter_fourcc(*"mp4v"), 
            fps, 
            (width, height)
        )

        for _ in tqdm(iterable=range(total_frames), 
                      desc="Processing video", 
                      unit="frame", 
                      ncols=100,
                      dynamic_ncols=True,
                      disable=not verbose):
            
            ret, frame = video.read()
            if not ret:
                break

            for augmentation in augmentations.values():
                frame = np.array(augmentation(Image.fromarray(frame)))

            writer.write(frame)

        video.release()
        writer.release()


        if verbose:
            print("Augmentation complete.")