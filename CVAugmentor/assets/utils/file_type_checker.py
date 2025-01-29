import mimetypes


def is_target_type(filename: str, target: str) -> bool:

    """

    Checks if the file is of the target type.


    Parameters
    ----------
    filename : str
        Name of the file.

    target : str
        Target type.

    
    Returns
    -------
    bool
        True if the file is of the target type, False otherwise.

    """

    if not isinstance(filename, str):
        raise ValueError("filename must be a string")
    if not isinstance(target, str):
        raise ValueError("target must be a string")
    

    # Get the mime type
    mime_type = mimetypes.guess_type(filename)[0]


    # Return True if the mime type is not None and starts with the target type
    return bool(mime_type) and mime_type.startswith(f'{target}/')