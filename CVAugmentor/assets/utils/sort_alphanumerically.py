import re


def sorted_alphanumerically(input_list: list[str]) -> list[str]:

    """

    Sorts a list alphanumerically.

    
    Parameters
    ----------
    input_list : list
        The unordered list.

    
    Returns
    -------
    output_list : list
        The sorted list. 

    """

    if not isinstance(input_list, list) or not all(isinstance(string, str) for string in input_list):
        raise ValueError("input_list must be a list of strings")
    

    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 


    return sorted(input_list, key=alphanum_key)