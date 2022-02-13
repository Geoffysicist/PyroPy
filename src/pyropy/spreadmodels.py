"""spreadmodels.py

Australian rate of spread models for wildfire and prescribed burns.

Unless otherwise indicated all models have been taken from:

> Cruz, Miguel, James Gould, Martin Alexander, Lachie Mccaw, and Stuart Matthews. 
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
can be added as a parameter. TODO add error checking for this!

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
    """Forward Rate of Spread (FROS) from McArthur Mk5 Forest Fire Danger Meter.
    
    Eqn: 5.27

    Application: Wildfire in Sclerophyll (Eucalypt) forests
   
    Notes: This model is still widely used by FBAns in Australia though 
    Cruz et al. 2015 recommend using Vesta in preference. However many 
    FBAns feel that Vesta over predicts ROS unless conditions are 
    severe.

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        wrf: wind reduction factor
        fuel_load: fine fule load t/ha

    Returns:
        a pandas dataframe including the fields
            
            `fros_mk5` the forward rate of spread (m/h)
    """
    ros_df = df.copy(deep=True)
    
    #TODO should we always calculate this?
    if not ('ffdi' in ros_df.columns): ros_df['ffdi'] = get_FFDI(df, wrf)

    ros_df['fros_mk5'] = 0.0012*ros_df['ffdi']*fuel_load*1000 #convert to m/h

    return ros_df

def ros_forest_vesta(
        df: DataFrame,
        fhs_surf: float,
        fhs_n_surf: float,
        fuel_height_ns: float, #cm
    ) -> DataFrame:
    """Forward Rate of Spread (FROS) from Project Vesta (fuel hazard scores)

    Eqn: 5.28

    Application: Wildfire in Sclerophyll (Eucalypt) forests
   
    Notes: Many FBAns feel that Vesta over predicts ROS unless conditions
    are severe and use McArthur 1973a Mk5 Forest Fire Danger Meter.

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        fhs_surf: surface fuel hazard score (0-4)
        fhs_n_surf: near surface fuel hazard score (0-4)
        fuel_height_ns: near surface fuel height (cm)

    Returns:
        a pandas dataframe including the fields

            `mc` the fuel moisture conent (%)
            `fros_vesta` the forward rate of spread (m/h)
    """

    # determine moisture content
    #TODO tidy this with df.where
    ros_df = df.copy(deep=True)


    ros_df['mc'] = np.where(
        (ros_df['date_time'].dt.hour >= 9) & (ros_df['date_time'].dt.hour < 20),
        np.where(
            (ros_df['date_time'].dt.hour >= 12) & (ros_df['date_time'].dt.hour < 17), 
            2.76 + (0.124*ros_df['humidity']) - (0.0187*ros_df['temp']), 
            3.6 + (0.169*ros_df['humidity']) - (0.045*ros_df['temp'])
        ),
        3.08 + (0.198*ros_df['humidity']) - (0.0483*ros_df['temp'])
    )

    # determine moisture function
    mf = 18.35 * ros_df['mc']**-1.495

    # determine the ROS
    ros_df['fros_vesta'] = np.where(
        ros_df['wind_speed'] > 5,
        30.0 + 1.531 * (ros_df['wind_speed']-5)**0.8576 * fhs_surf**0.93 * (fhs_n_surf*fuel_height_ns)**0.637 * 1.03,
        30
    )

    ros_df['fros_vesta'] = ros_df['fros_vesta']* mf
    return ros_df

def spread_direction(df: DataFrame) -> Series:
    """ Converts wind direction to spread direction.
    
    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)

    Returns:
        a pandas Series of spread direction in degrees.
    """
    fros_dir = np.where(
        df['wind_dir'] < 180,
        df['wind_dir'] + 180,
        df['wind_dir'] - 180
    )

    return Series(fros_dir)

def get_FFDI(
        df: DataFrame, 
        wrf: int = 3, 
        flank: bool=False, 
        DF: int=9,
    ) -> Series:
    """McArthur Forest Fire Danger Index (FFDI).
    
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
        DF: drought factor, this is only used if there is no `drought` in the 
            DataFrame

    Returns:
        a pandas Series of FFDI.

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

#templates - not in documentation
def _ros_template(
        df: DataFrame, 
        arg1: object, 
        arg2: object,
    ) -> DataFrame:
    """Forward Rate of Spread (FROS) from model_name.
    
    Eqn: N.NN

    Application: vetetation type
   
    Notes: anything else about the model.

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        arg1: whatever arg1 represents (units)
        arg2: whatever arg2 represents (units)

    Returns:
        a pandas dataframe including the fields
        
            `fros_template` the forward rate of spread (m/h)
            `field1` description of field 1
            `field2` description of field 2.
    """

    pass