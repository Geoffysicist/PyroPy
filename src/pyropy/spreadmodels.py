"""
Australian rate of spread models for wildfire and prescribed burns.

Unless otherwise indicated all models have been taken from:
Cruz, Miguel, James Gould, Martin Alexander, Lachie Mccaw, and Stuart Matthews. 
(2015) A Guide to Rate of Fire Spread Models for Australian Vegetation, 
CSIRO Land & Water and AFAC, Melbourne, Vic 125 pp. 

Unless otherwise indicated all equations numbers also refer to Cruz et al. 2015.

All spread models take a pandas weather dataframe and model specific 
parmeters as arguments.

The weather dataframe must include the following exact fields (column headings):
```
    date_time: a pandas datetime field
    temp: Air temerature (°C)
    humidity: Relative humidity (%)
    wind_speed: 10 m wind speed (km/h)
    wind_dir: Wind direction (°)
```
Ideally the weather dataframe should include a drought factor though this
can be added as a parameter. TODO error checking for this!

The `weather` module provides function for reading `*.csv` files into 
dataframes from standard sources
"""

# TODO:
# - add flame hight and intensity
# = flank ROS from length to breadth ratio

import numpy as np
from pandas import DataFrame, Series

def ros_forest_mk5(
        df: DataFrame, 
        wrf: float, 
        fuel_load: float,
    ) -> DataFrame:
    """Predicts the FROS from McArthur 1973a Mk5 Forest Fire Danger Meter.

    Uses Eqn 5.27

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        wrf: wind reduction factor
        fuel_load: fine fule load t/ha

    Returns:
        a pandas dataframe including the fields `fros_mk5` the forward
        rate of spread (km/h), `fros_dir` the direction of spread, and `ffdi`
        the forest fire danger index.
    
    TODO use leaflet 80 when FFDI < 12
    """
    ros_df = df.copy(deep=True)
    ros_df['fros_dir'] = spread_direction(df)
    
    #TODO use BOM FFDI if supplied?
    ros_df['ffdi'] = get_FFDI(df, wrf)

    ros_df['fros_mk5'] = 0.0012*ros_df['ffdi']*fuel_load

    return ros_df

def ros_forest_vesta(
        df: DataFrame,
        fhs_surf: float,
        fhs_n_surf: float,
        fuel_height_ns: float, #cm
    ) -> DataFrame:
    """Project Vesta Cheney et al 2012.

    using fuel hazard scores Eq 5.28
    """

    # determine moisture content
    #TODO tidy this with df.where
    df['mc'] = np.where(
        (df['date_time'].dt.hour >= 9) & (df['date_time'].dt.hour < 20),
        np.where(
            (df['date_time'].dt.hour >= 12) & (df['date_time'].dt.hour < 17), 
            2.76 + (0.124*df['humidity']) - (0.0187*df['temp']), 
            3.6 + (0.169*df['humidity']) - (0.045*df['temp'])
        ),
        3.08 + (0.198*df['humidity']) - (0.0483*df['temp'])
    )

    # determine moisture function
    df['mf'] = 18.35 * df['mc']**-1.495

    # determine the ROS
    # df['ros'] = 30.0 * df['mf'] / 1000
    df['fros_vesta'] = np.where(
        df['wind_speed'] > 5,
        30.0 + 1.531 * (df['wind_speed']-5)**0.8576 * fhs_surf**0.93 * (fhs_n_surf*fuel_height_ns)**0.637 * 1.03,
        30
    )

    df['fros_vesta'] = df['fros_vesta']* df['mf']
    return df

#Additional functions TODO to helpers?
def spread_direction(weather_df: DataFrame) -> DataFrame:
    """ Converts wind direction to spread direction"""

    return np.where(
        weather_df['wind_dir'] < 180,
        weather_df['wind_dir'] + 180,
        weather_df['wind_dir'] - 180
    )

def get_FFDI(df: DataFrame, wrf: int = 3, flank=False, DF=9) -> Series:
    """Calculates FFDI.
    
    Uses Eqn 5.19.

    If a drought factor (column heading = `drought`) is present in the weather
    dataframe then this is used, otherwise a drought factor must be supplied or
    the drought factor defaults to 9.

    if `flank=True` the ffdi is calculated for a wind speed = 0

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        wrf: a wind reduction factor
        flank: if `flank=True` the ffdi is calculated for a wind speed = 0
        DF: drought factor, this is only used if there is no `drought` in the weather

    Returns:
        a pandas Series that can be added to an existing Incident dataframe.

    Raises:
        no errors 
    """
    if flank:
        wind_speed = 0
    else:
        wind_speed = df['wind_speed']

    if not ('drought' in df.columns): df['drought'] = DF

    ffdi = 2.0*np.exp(
        -0.450 + 0.987*np.log(df['drought'])
        -0.0345*df['humidity']
        +0.0338*df['temp']
        +0.0234* wind_speed * 3 / wrf 
        )
    
    return np.round(ffdi, 1)
