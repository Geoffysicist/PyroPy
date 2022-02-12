from pandas import DataFrame
import pytest
import warnings

from src.pyropy import weather_data as wd

def test_weather_to_df():
    fn = 'tests/.data/weather_base_in.csv'
    assert type(wd.weather_to_df(fn)) is DataFrame

def test_gridded_to_df():
    fn = 'tests/.data/weather_gridded_in.csv'
    assert type(wd.weather_to_df(fn)) is DataFrame

def test_df_to_weather():
    fn = 'tests/.data/weather_gridded_in.csv'
    df = wd.gridded_to_df(fn)
    assert type(df) is DataFrame
    out_fn = 'tests/.data/weather_base_out.csv'
    out_df = wd.df_to_weather(df,out_fn)
    assert type(out_df) is DataFrame
    with open(out_fn, 'r') as f:
        assert 'Date time' in f.readlines()[0]    