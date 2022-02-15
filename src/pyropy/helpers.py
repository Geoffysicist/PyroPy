"""Utility scripts for fire behaviour analysis."""
import os
import warnings
from openpyxl import Workbook, load_workbook

# if  __name__ == '__main__':
#     from firebehaviour import Incident
# else:
#     from .firebehaviour import Incident

def check_filepath(fn: str, suffix: str = None) -> bool:
    valid = os.path.isfile(fn)
    if not valid: warnings.warn(f'{fn} is not a valid filename')
    if suffix:
        fn = fn.split('.')
        valid = (fn[-1] == suffix)
        if not valid: warnings.warn(f'file must be a *.{suffix} file')
    return valid

def check_encoding(fn: str) -> str:
    """Returns the encoding of a csv file.
    
    TODO if encoding is Windws cp1252 change to latin-1 for better mapping see 
    http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
    """
    with open(fn) as f:
        return(f.encoding)






if __name__ == '__main__':
    pass
