import logging

PACKAGE_LOGGER_NAME = "cvaugmentor"


def get_logger(suffix: str | None = None) -> logging.Logger:

    """

    Returns a child of the package logger.


    Usage
    -----
    Libraries must never configure handlers, levels, or formats on behalf of
    the embedding application. The package root logger carries a NullHandler
    (attached in the package `__init__`), so pipeline logs stay silent until
    the application opts in by configuring logging itself.
    ```python
    from cvaugmentor.core.logging import get_logger

    logger = get_logger("services.augmentation")
    logger.debug("This is silent unless the host application configures logging.")
    ```


    Parameters
    ----------
    suffix : str | None, optional
        The dotted path appended to the package logger name.


    Returns
    -------
    logging.Logger
        The resolved logger instance.


    Raises
    ------
    TypeError
        If `suffix` is not a string.

    """

    if suffix is not None and not isinstance(suffix, str):
        raise TypeError(f"suffix must be a string. Received: {suffix} with type {type(suffix)}")


    if not suffix:
        return logging.getLogger(PACKAGE_LOGGER_NAME)

    return logging.getLogger(f"{PACKAGE_LOGGER_NAME}.{suffix}")
