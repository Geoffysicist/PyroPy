from pandas import DataFrame
import pytest
import warnings

from src.firebehaviour import spreadmodels as fs
from src.firebehaviour import weather_data as wd

@pytest.fixture
def mock_weather():
    fn = 'tests/.data/weather_gridded_in.csv'
    return wd.gridded_to_df(fn)


def test_ros_forest_mk5(mock_weather):
    df = fs.ros_forest_mk5(mock_weather, 3, 15)
    assert type(df) is DataFrame
    assert 'fros_mk5' in df.columns.values.tolist()

