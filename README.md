# PyroPy
Analysis of fire spread and intensity

## Reading weather data
The weather data is read into a pandas dataframe from a `*.csv` file.
The fire behaviour models require certain fields to be present in the weather data and these are mapped using dictionaries.
There are several standard mappings included (see below), but for non-standard data users must create their own dictionary and supply that as an argument to the `weather_to_df` function. The mapping dictionary must contain the keys in the `FIELDS_BASE` dictionary as a minimum.

There are functions to handle the standard data formats such as BOM gridded weather with mapping dictionaries already defined.
```python
gridded_to_df(fn)
amicus_to_df(fn)
df_to_gridded(fn)
df_to_amicus(fn)
```

For example, if you are using BOM gridded weather data the you should run:
```python
df = gridded_to_df('your_file_path.csv')
```

### `Base` weather data structure
call the function `weather_to_df(fn)`
```python
FIELDS_BASE = {
    'date_time': 'Date time',
    'temp': 'Air temperature (C)',
    'humidity': 'Relative humidity (%)',
    'wind_speed': '10 m wind speed (km/h)',
    'wind_dir': 'Wind direction',
    'wind_dir_cp': 'Wind direction',
    'drought': 'Drought Factor',
    'ffdi': 'FFDI',
    'gfdi': 'GFDI',
    'dewpoint': 'dew_temp',
    'fuel_state': 'fuel_state',
}
```

### `Gridded` weather data structure
call the function `gridded_to_df(fn)`
```python
FIELDS_GRIDDED = {
    'date': 'Local Date',
    'time': 'Local Time',
    'temp': 'Temp (C)',
    'humidity': 'RH (%)',
    'wind_dir': 'Wind Dir',
    'wind_speed': 'Wind Speed (km/h)',
    'drought': 'Drought Factor',
    'ffdi': 'FFDI',
    'gfdi': 'GFDI',
}
```