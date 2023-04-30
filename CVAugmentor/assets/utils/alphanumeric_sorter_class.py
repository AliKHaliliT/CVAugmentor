# Importing the libraries
import re


# Defining the alphanumeric sorter class
class AlphanumericSorter():

    # Defining the constructor
    def __init__(self) -> None:

        '''
        
        Parameters
        ----------
        None.

        
        Returns
        -------
        None.

        '''
        
        pass


    # Sorting the list alphanumerically
    def sorted_alphanumeric(self, data: list) -> list:

        '''
        
        Parameters
        ----------
        data : list

        
        Returns
        -------
        sorted_data : list

        '''
        
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 


        return sorted(data, key=alphanum_key)