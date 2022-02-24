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

def test_get_mc_v(mock_weather):
    """Vesta fine fuel moisture content."""
    mc = fs.get_mc_v(mock_weather)
    assert type(mc) is Series
    assert not mc.empty

def test_get_mc_g(mock_weather):
    """Grass fine fuel moisture content."""
    mc = fs.get_mc_g(mock_weather)
    assert type(mc) is Series
    assert not mc.empty

def test_get_mc_m(mock_weather):
    """Mallee fine fuel moisture content."""
    mc = fs.get_mc_m(mock_weather)
    assert type(mc) is Series
    assert not mc.empty

def test_ros_forest_mk5(mock_weather):
    df = fs.ros_forest_mk5(mock_weather, 3, 15)
    assert type(df) is DataFrame
    assert 'fros_mk5' in df.columns.values

def test_ros_forest_vesta(mock_weather):
    df = fs.ros_forest_vesta(mock_weather, 3, 3, 15)
    assert type(df) is DataFrame
    assert 'fros_vesta' in df.columns.values

def test_ros_forest_vesta_fhr(mock_weather):
    df = fs.ros_forest_vesta_fhr(mock_weather, 'H', 'M')
    assert type(df) is DataFrame
    assert 'fros_vesta_fhr' in df.columns.values

def test_ros_forest_vesta2(mock_weather):
    df = fs.ros_forest_vesta2(mock_weather, 3, 14, 0.8)
    assert type(df) is DataFrame
    assert 'fros_vesta2' in df.columns.values

def test_ros_grass(mock_weather):
    df = fs.ros_grass(mock_weather, 'E', 90)
    assert type(df) is DataFrame
    assert 'fros_grass' in df.columns.values
    assert 'mc_g' in df.columns.values

def test_ros_mallee(mock_weather):
    df = fs.ros_mallee(mock_weather, 30, 5)
    assert type(df) is DataFrame
    assert 'fros_mallee' in df.columns.values
    assert 'mc_m' in df.columns.values
