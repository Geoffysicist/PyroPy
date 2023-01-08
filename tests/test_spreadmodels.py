import pytest
from pandas import DataFrame, Series

from src.pyropy import spreadmodels as pps
from src.pyropy import helpers as pph
from src.pyropy import weatherdata as ppw

logger = pph.get_logger()

@pytest.fixture
def mock_weather():
    fn = 'tests/.data/weather_gridded_in.csv'
    return ppw.gridded_to_df(fn)

def test_FFDI(mock_weather):
    df = mock_weather
    ffdi = pps.FFDI(df.temp, df.humidity, df.wind_speed, df.drought, wrf = 3.5)
    assert type(ffdi) is Series
    assert not ffdi.empty

def test_ros_forest_mk5(mock_weather):
    df = mock_weather
    ffdi = pps.FFDI(df.temp, df.humidity, df.wind_speed, df.drought, wrf = 3.5)
    ros = pps.ros_forest_mk5(ffdi, 10)
    assert type(ros) is Series
    assert not ros.empty

def test_mc_vesta(mock_weather):
    df = mock_weather
    mc = pps.mc_vesta(df.date_time, df.temp, df.humidity)
    assert type(mc) is Series
    assert not mc.empty
