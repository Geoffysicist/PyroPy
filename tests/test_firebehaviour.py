from pandas import DataFrame, Series
import pytest
import warnings
from random import randrange

from src.pyropy import firebehaviour as fb
from src.pyropy import weatherdata as wd

@pytest.fixture
def mock_weather():
    fn = 'tests/.data/weather_gridded_in.csv'
    return wd.gridded_to_df(fn)

def test_incident(mock_weather):
    assert type(fb.Incident(mock_weather).df) is DataFrame


@pytest.fixture
def mock_incident(mock_weather):
    return fb.Incident(mock_weather)

def test_get_params(mock_incident):
    mock_incident.waf = 4
    params = mock_incident.get_params()
    assert type(params) is dict
    assert params['waf'] == 4

def test_check_params(mock_incident):
    warnings.simplefilter('always') #catch all warnings always
    params = {'foo': 15}
    with warnings.catch_warnings(record=True) as w:        
        mock_incident.check_params(params) 
        assert 'not set - run set params' in str(w[-1].message)


def test_set_params(mock_incident):
    params = {
            'waf': randrange(6),
            'fuel_load': randrange(25),
        }
    mock_incident.set_params(params)
    assert mock_incident.waf == params['waf']
    assert mock_incident.fuel_load == params['fuel_load']


def test_run_forest_mk5(mock_incident):
    forest_mk5_params = {
        'waf': 3.5,
        'fuel_load': 15,
    }
    mock_incident.set_params(forest_mk5_params)
    mock_incident.run_forest_mk5()
    assert 'fros_mk5' in mock_incident.df.columns.values

def test_run_forest_vesta(mock_incident):
    forest_vesta_params = {
        'fhs_surf': 3.5,
        'fhs_n_surf': 2,
        'fuel_height_ns': 20
    }
    mock_incident.set_params(forest_vesta_params)
    mock_incident.run_forest_vesta()
    assert 'fros_vesta' in mock_incident.df.columns.values

def test_run_forest_vesta2(mock_incident):
    forest_vesta_params = {
        'waf': 3,
        'fuel': 14,
        'fuel_height_u': 0.8
    }
    mock_incident.set_params(forest_vesta_params)
    mock_incident.run_forest_vesta2()
    assert 'fros_vesta2' in mock_incident.df.columns.values

def test_run_forest_vesta_fhr(mock_incident):
    forest_vesta_params = {
        'fhr_surf': 'H',
        'fhr_n_surf': 'M',
    }
    mock_incident.set_params(forest_vesta_params)
    mock_incident.run_forest_vesta_fhr()
    assert 'fros_vesta_fhr' in mock_incident.df.columns.values


@pytest.fixture
def mock_incident(mock_weather):
    mock_incident =  fb.Incident(mock_weather)
    forest_params = {
        'waf': 3.5,
        'fuel_load': 15,
        'fhs_surf': 3.5,
        'fhs_n_surf': 2,
        'fuel_height_ns': 20
    }
    mock_incident.set_params(forest_params)
    mock_incident.run_forest_mk5()
    # mock_incident.run_forest_vesta()

    return mock_incident


def test_get_models(mock_incident):
    assert set(['forest_mk5']).issubset(
            set(mock_incident.get_models())
        )

def test_compare_fbcalc(mock_incident):
    calc_fn = 'tests/.data/FireBehaviourCalcs_Test.xlsm'
    models = ['vesta']
    mock_incident.compare_fbcalc(calc_fn, models)
    assert set(['fros_vesta','fros_vesta_fbcalc']).issubset(
        set(mock_incident.df.columns.values)
    )
    
def test_set_fbcalc(mock_incident):
    calc_fn = 'tests/.data/FireBehaviourCalcs_Test_out.xlsm'
    ws = mock_incident.set_fbcalc(calc_fn)
    assert ws is True
    
    


