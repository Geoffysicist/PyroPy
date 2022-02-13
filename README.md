# PyroPy
Analysis of fire spread and intensity.

Author: Geoffysicist

Source code: [https://github.com/Geoffysicist/PyroPy](https://github.com/Geoffysicist/PyroPy)

Uses weather data and model specific parameters to predict rate of spread and intensity of wildfires.

## Modules
 - firebehaviour: Defines the main `Incident` class and several auxillary dictionaries. An `Incident` stores data related to the incident including weather, model parameters and model outputs.
 - spreadmodels: fire spread model functions which can be called directly or by an `Incident`.
 - weatherdata: functions for reading, writing and transforming weather between various formats including Australian Bureau of Meteorology (BoM) Gridded Weather, BoM Observations (*.axf) and Amicus.
 - helpers: various helper functions for file handling and data processing

for more detailed information see [modules](modules.md)

## Typical Use
```python
from pyropy import firebehaviour as fb
from pyropy import weather_data as wd

if __name__ == '__main__':
   #read the weather data into a pandas DataFrame
   weather_fn = 'tests/.data/weather_gridded_in.csv'
   weather_df = wd.gridded_to_df(weather_fn)

   #create an Incident using the weather data
   incident = fb.Incident(weather_df)

   #add the parameters necessary to run the desired models
   incident_params = {
      #forest_mk5
      'wrf': 3.5,
      'fuel_load': 15,
      #forest_vesta
      'fhs_surf': 3.5,
      'fhs_n_surf': 2,
      'fuel_height_ns': 20
   }
   incident.update_params(incident_params)

   #run the desired models
   incident.run_forest_mk5()
   incident.run_forest_vesta()

   #output results
   incident.print()
```

## Fire Spread Models
Unless otherwise indicated all models have been taken from:
> Cruz, Miguel, James Gould, Martin Alexander, Lachie Mccaw, and Stuart Matthews. 
(2015) A Guide to Rate of Fire Spread Models for Australian Vegetation, 
CSIRO Land & Water and AFAC, Melbourne, Vic 125 pp. 

Unless otherwise indicated all equations numbers also refer to Cruz et al. 2015.

All spread models take a pandas weather dataframe and model specific 
parmeters as arguments.

## Weather Data
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