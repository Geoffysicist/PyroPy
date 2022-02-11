from pandas import DataFrame
import pytest
import warnings

from src.firebehaviour import helpers

def test_check_filepath():
    assert helpers.check_filepath('tests/.data/weather_gridded_in.csv') is True
    warnings.simplefilter('always') #catch all warnings always
    with warnings.catch_warnings(record=True) as w:        
        helpers.check_filepath('foo') 
        assert 'not a valid filename' in str(w[-1].message)
    
    with warnings.catch_warnings(record=True) as w:        
        helpers.check_filepath('tests/.data/utf_8.csv', suffix='bar')
        assert 'file must be' in str(w[-1].message)

def test_check_encoding():
    assert helpers.check_encoding('tests/.data/utf_8.csv') == 'UTF-8'    
    assert helpers.check_encoding('tests/.data/macintosh.csv') == 'UTF-8'    
    assert helpers.check_encoding('tests/.data/ms_dos.csv') == 'UTF-8'
