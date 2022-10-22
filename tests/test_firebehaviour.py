from typing import is_typeddict
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
    mock_incident.run_forest_vesta(version_12=False)
    assert 'fros_vesta_08' in mock_incident.df.columns.values

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

def test_run_grass(mock_incident):
    grass_params = {
        'grass_state': 'G',
        'curing': 90,
    }
    mock_incident.set_params(grass_params)
    mock_incident.run_grass()
    assert 'fros_grass' in mock_incident.df.columns.values

def test_run_mallee(mock_incident):
    mallee_params = {
        'cover_o': 20,
        'height_o': 3.5,
    }
    mock_incident.set_params(mallee_params)
    mock_incident.run_mallee()
    assert 'fros_mallee' in mock_incident.df.columns.values



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
    models = ['mk5','vesta', 'vesta2', 'mallee']
    fbcalc_params = mock_incident.compare_fbcalc(calc_fn, models)
    assert set([
        'fros_mk5_fbcalc',
        'fros_vesta_fbcalc',
        'fros_vesta2_fbcalc',
        'fros_mallee_fbcalc',
    ]).issubset(set(mock_incident.df.columns.values)
    )
    assert isinstance(fbcalc_params, dict)
    
def test_set_fbcalc(mock_incident):
    calc_fn = 'tests/.data/FireBehaviourCalcs_Test_out.xlsm'
    ws = mock_incident.set_fbcalc(calc_fn)
    assert ws is True
    
def test_get_spread_direction(mock_incident):
    mock_incident.get_spread_direction()
    assert set(['spread_dir']).issubset(
        set(mock_incident.df.columns.values)
    )


