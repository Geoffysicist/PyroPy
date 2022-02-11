from pandas import DataFrame, Series
import pytest
import warnings

from src.firebehaviour import firebehaviour as fb
from src.firebehaviour import weather_data as wd

@pytest.fixture
def mock_weather():
    fn = 'tests/.data/weather_gridded_in.csv'
    return wd.gridded_to_df(fn)

def test_incident(mock_weather):
    assert type(fb.Incident(mock_weather).df) is DataFrame

@pytest.fixture
def mock_incident(mock_weather):
    return fb.Incident(mock_weather)

def test_update_params(mock_incident):
    assert type(mock_incident) is fb.Incident
    assert mock_incident.wrf is None
    params = {
            'wrf': 3,
            'fuel_load': 15,
        }
    mock_incident.update_params(params)
    assert mock_incident.wrf == params['wrf']

    # warnings.simplefilter('always') #catch all warnings always
    # with warnings.catch_warnings(record=True) as w:        
    #     mock_incident.run_forest_mk5() 
    #     assert 'not set - run update params' in str(w[-1].message)


def test_run_forest_mk5(mock_incident):
    assert type(mock_incident) is fb.Incident

    warnings.simplefilter('always') #catch all warnings always
    with warnings.catch_warnings(record=True) as w:        
        mock_incident.run_forest_mk5() 
        assert 'not set - run update params' in str(w[-1].message)
    


