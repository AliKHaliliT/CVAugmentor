# Import the libraries
import mimetypes


# Defining the FileChecker class
class FileTypeChecker():

    """
    
    Class that checks the file type.
    
    """

    # Defining the constructor
    def __init__(self) -> None:
            
        """

        Constructor of the FileChecker class.

        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.
        
        """

        pass


    # Defining the is_target_type method
    def is_target_type(self, filename: str, target: str) -> bool:

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

        # Get the mime type
        mime_type, _ = mimetypes.guess_type(filename)


        # Return True if the mime type is not None and starts with the target type
        return mime_type is not None and mime_type.startswith(f'{target}/')