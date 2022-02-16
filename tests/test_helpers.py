from openpyxl import Workbook
from pandas import DataFrame
import pytest
import warnings

from src.pyropy import helpers
from src.pyropy import firebehaviour as fb
from src.pyropy import weatherdata as wd


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
    assert helpers.check_encoding('tests/.data/cp1252.csv') == 'cp1252'    
    assert helpers.check_encoding('tests/.data/macintosh.csv') == 'cp1252'    
    assert helpers.check_encoding('tests/.data/ms_dos.csv') == 'cp1252'

@pytest.fixture
def mock_incident():
    fn = 'tests/.data/weather_gridded_in.csv'
    weather_df = wd.gridded_to_df(fn)
    return fb.Incident(weather_df)


# def test_incident_to_calc(mock_incident):
#     fn = 'tests/.data/FireBehaviourCalcs_Test.xlsm'
#     wb = helpers.incident_to_calc(mock_incident,fn)
#     assert type(wb) is Workbook