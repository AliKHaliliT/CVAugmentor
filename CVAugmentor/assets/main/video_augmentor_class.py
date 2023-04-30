# Importing the libraries
from typing import Dict, Callable, Optional
import cv2
from tqdm import tqdm
import os
import numpy as np
from PIL import Image


# Defining the VideoAugmentor class
class VideoAugmentor():

    # Defining the constructor
    def __init__(self) -> None:
        
        """

        Constructor of the VideoAugmentor class.
        
        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    # Defining the augment method
    def augment_one_by_one(self, video_path: str, output_path: str, augmentations: Dict[str, Callable], verbose: Optional[bool] = False) -> None:
            
        """

        Augments the video one augmentation at a time.
        This means that the video will be augmented by the first augmentation, then it will be saved. 
        Next the video will be augmented by the second augmentation, then it will be saved. And so on.

        
        Parameters
        ----------
        video_path : str
            Path to the video file to be augmented.

        output_path : str
            Path to the output video file.

        augmentations : dict
            Dict of augmentations to be applied to the video. 
            The keys are the names of the augmentations and the values are the augmentations themselves.

        verbose : bool, optional
            If True, prints the progress of the augmentation process. The default is False.

        
        Returns
        -------
        None.
        
        """

        # Load the video and get its properties
        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


        # Initialize the outer progress bar
        outer_pbar = tqdm(total=len(augmentations), desc='Augmenting Video', unit=' Num_Augmentations', leave=False, dynamic_ncols=True, disable=not verbose)

        # Loop through the augmentations
        for name, augmentation in augmentations.items():

            # Set the video to the first frame
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)

            # Create a VideoWriter object
            writer = cv2.VideoWriter((os.path.splitext(output_path)[0] + "_" + name + os.path.splitext(output_path)[1]),
                                        cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))


            # Initialize the inner progress bar
            inner_pbar = tqdm(total=total_frames, desc='Augmentation Progress', unit=' Frames', leave=False, dynamic_ncols=True, disable=not verbose)

            # Loop through the frames
            for _ in range(total_frames):
    
                # Read the frame
                ret, frame = video.read()
    
                # Check if the frame was read successfully
                if ret:
    
                    # Apply the augmentation
                    frame = np.array(augmentation(Image.fromarray(frame)))
    
                    # Write the frame to the output video
                    writer.write(frame)

                    # Update the inner progress bar
                    inner_pbar.update()
                    
                else:
                    break


            # Release the writer
            writer.release()

            # Progress Bar Update
            inner_pbar.close()
            outer_pbar.update()


        # Release the video
        video.release()

        # Close the progress bar
        outer_pbar.close()


        if verbose:
            # Print a message
            print('Augmentation Completed!')


    # Defining the augment method
    def augment_all_at_once(self, video_path: str, output_path: str, augmentations: Dict[str, Callable], verbose: Optional[bool] = False) -> None:
        
        """

        Augments the video all at once.
        This means that the video will be augmented by all the augmentations at once, then it will be saved.

        
        Parameters
        ----------
        video_path : str
            Path to the video file to be augmented.

        output_path : str
            Path to the output video file.

        augmentations : dict
            Dict of augmentations to be applied to the video. 
            The keys are the names of the augmentations and the values are the augmentations themselves.

        verbose : bool, optional
            If True, prints the progress of the augmentation process. The default is False.

        
        Returns
        -------
        None.
        
        """

        # Load the video and get its properties
        video = cv2.VideoCapture(video_path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video.get(cv2.CAP_PROP_FPS))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


        # Create a VideoWriter object
        writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))


        # Initialize the outer progress bar
        outer_pbar = tqdm(total=total_frames, desc='Augmenting Video', unit=' Frames', leave=False, dynamic_ncols=True, disable=not verbose)

        # Loop through the frames
        for _ in range(total_frames):

            # Read the frame
            ret, frame = video.read()

            # Check if the frame was read successfully
            if not ret:
                break


            # Initialize the inner progress bar
            inner_pbar = tqdm(total=len(augmentations), desc='Augmentation Progress', unit=' Num_Augmentations', leave=False, dynamic_ncols=True, disable=not verbose)

            # Loop through the augmentations
            for _, augmentation in augmentations.items():

                # Apply the augmentation
                frame = np.array(augmentation(Image.fromarray(frame)))


                # Update the inner progress bar
                inner_pbar.update()

            # Write the frame to the output video
            writer.write(frame)


            # Progress Bar Update
            inner_pbar.close()
            outer_pbar.update()


        # Release the video
        video.release()

        # Release the writer
        writer.release()


        # Close the progress bar
        outer_pbar.close()

        if verbose:
            # Print a message
            print('Augmentation Completed!')