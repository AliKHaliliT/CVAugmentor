class AugmentationException(Exception):

    """

    Base augmentation exception.

    """

    pass


class PipelineConfigurationError(AugmentationException):

    """

    Raised when the pipeline is assembled with an invalid configuration.

    """

    pass


class DuplicateAugmentationError(AugmentationException):

    """

    Raised when an augmentation label is registered more than once.

    """

    pass


class UnsupportedMediaError(AugmentationException):

    """

    Raised when no codec handles the medium kind a job asks for.

    """

    pass


class MediaReadError(AugmentationException):

    """

    Raised when a medium cannot be decoded.

    """

    pass


class MediaWriteError(AugmentationException):

    """

    Raised when a medium cannot be encoded.

    """

    pass


class AugmentationExecutionError(AugmentationException):

    """

    Raised when an augmentation fails while transforming a frame.

    """

    pass
