from typing import Optional, Callable
import os
from .components.pipeline._choose_augmentor import _choose_augmentor
from .components.pipeline._process_single import _process_single
from .components.pipeline._process_batch import _process_batch


class Pipeline():

    def __init__(self) -> None:

        """

        Constructor of the Pipeline class.

        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    def _validate_inputs(self, 
                         input_path: str, 
                         output_path: str, 
                         target: str, 
                         process_type: str, 
                         mode: str,
                         verbose: Optional[bool] = False, 
                         warn_verbose: Optional[bool] = True,
                         random_state: Optional[bool] = False) -> None:
        
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
                    "single"
                        Single type means that the input and output paths are files.
                    "batch"
                        Batch type means that the input and output paths are directories.

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
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            If True, prints the overall progress of the augmentation process. The default value is `False`.

        aug_verbose : bool, optional
            If True, prints the progress of the augmentation process. The default value is `False`.

        warn_verbose : bool, optional
            If True, prints the warnings. The default value is `True`.

        random_state : bool, optional
            When set to `True`, it resets the states of the augmentations. The default value is `False`.
            This means that for any parameters that were randomly selected, new random values will be assigned. 
            This functionality is particularly useful when augmenting a dataset where you want each sample to undergo the same augmentation process but with varying random behavior. 
            However, you should only enable this option (`True`) if your augmentation dictionary contains unspecified parameters. 
            Otherwise, setting it to `True` may introduce unnecessary overhead.

        
        Returns
        -------
        None.
        
        """
        
        if not isinstance(input_path, str) or not os.path.exists(input_path):
            raise ValueError(f"input_path must be a valid string and exist. Received: {input_path} with type {type(input_path)}")
        if not isinstance(output_path, str) or not os.path.exists(os.path.dirname(output_path)):
            raise ValueError(f"output_path must be valid. Received: {output_path} with type {type(output_path)}")
        if target not in ["image", "video"]:
            raise ValueError(f"target must either be 'image' or 'video'. Received: {target} with type {type(target)}")
        if process_type not in ["single", "batch"]:
            raise ValueError(f"process_type must either be 'single' or 'video'. Received: {process_type} with type {type(process_type)}")
        if mode not in ["sequential", "singular"]:
            raise ValueError(f"mode must either be 'sequential' or 'singular'. Received: {mode} with type {type(mode)}")
        if not isinstance(verbose, bool):
            raise ValueError(f"verbose must be a boolean. Received: {verbose} with type {type(verbose)}")
        if not isinstance(warn_verbose, bool):
            raise ValueError(f"verbose must be a boolean. Received: {warn_verbose} with type {type(warn_verbose)}")
        if not isinstance(random_state, bool):
            raise ValueError(f"verbose must be a boolean. Received: {random_state} with type {type(random_state)}")


    def augment(self, 
                input_path: str, 
                output_path: str, 
                target: str, 
                process_type: str, 
                mode: str,
                augmentations: dict[str, Callable[..., None]], 
                verbose: Optional[bool] = False, 
                aug_verbose: Optional[bool] = False, 
                warn_verbose: Optional[bool] = True,
                random_state: Optional[bool] = False) -> None:
        
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
                    "single"
                        Single type means that the input and output paths are files.
                    "batch"
                        Batch type means that the input and output paths are directories.

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
            A dictionary of augmentations to apply. Keys are augmentation names, and values are the corresponding functions.

        verbose : bool, optional
            If True, prints the overall progress of the augmentation process. The default value is `False`.

        aug_verbose : bool, optional
            If True, prints the progress of the augmentation process. The default value is `False`.

        warn_verbose : bool, optional
            If True, prints the warnings. The default value is `True`.

        random_state : bool, optional
            When set to `True`, it resets the states of the augmentations. The default value is `False`.
            This means that for any parameters that were randomly selected, new random values will be assigned. 
            This functionality is particularly useful when augmenting a dataset where you want each sample to undergo the same augmentation process but with varying random behavior. 
            However, you should only enable this option (`True`) if your augmentation dictionary contains unspecified parameters and this functionality is absolutely necessary.
            Otherwise, setting it to `True` may introduce unnecessary overhead.
        
            
        Returns
        -------
        None.
        
        """

        self._validate_inputs(input_path, 
                              output_path, 
                              target, 
                              process_type, 
                              mode,
                              verbose, 
                              warn_verbose,
                              random_state)
        

        augmentor = _choose_augmentor(target)
        
        if process_type == "single":
            _process_single(input_path, 
                            target, 
                            output_path, 
                            mode, 
                            augmentor, 
                            augmentations, 
                            aug_verbose)
        elif process_type == "batch":
            _process_batch(input_path, 
                           verbose,
                           target, 
                           warn_verbose,
                           output_path,
                           mode, 
                           augmentor, 
                           augmentations, 
                           aug_verbose,
                           random_state)