from pandas import DataFrame, Series
import pytest
import warnings

from src.pyropy import spreadmodels as fs
from src.pyropy import weatherdata as wd

@pytest.fixture
def mock_weather():
    fn = 'tests/.data/weather_gridded_in.csv'
    return wd.gridded_to_df(fn)

def test_spread_direction(mock_weather):
    fros_dir = fs.spread_direction(mock_weather)
    assert type(fros_dir) is Series
    assert not fros_dir.empty

def test_get_FFDI(mock_weather):
    ffdi = fs.get_FFDI(mock_weather)
    assert type(ffdi) is Series
    assert not ffdi.empty

def test_get_mc(mock_weather):
    mc = fs.get_mc(mock_weather)
    assert type(mc) is Series
    assert not mc.empty

def test_ros_forest_mk5(mock_weather):
    df = fs.ros_forest_mk5(mock_weather, 3, 15)
    cols = ['fros_mk5']
    assert type(df) is DataFrame
    assert set(cols).issubset(set(df.columns.values.tolist()))

def test_ros_forest_vesta(mock_weather):
    df = fs.ros_forest_vesta(mock_weather, 3, 3, 15)
    cols = ['mc', 'fros_vesta']
    assert type(df) is DataFrame
    assert set(cols).issubset(set(df.columns.values.tolist()))

def test_ros_forest_vesta_fhr(mock_weather):
    df = fs.ros_forest_vesta_fhr(mock_weather, 'H', 'M')
    cols = ['mc', 'fros_vesta_fhr']
    assert type(df) is DataFrame
    assert set(cols).issubset(set(df.columns.values.tolist()))
