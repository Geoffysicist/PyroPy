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
import math as m

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
    # if not ('ffdi' in ros_df.columns): ros_df['ffdi'] = get_FFDI(df, wrf)
    ros_df['ffdi'] = get_FFDI(df, wrf)

    ros_df['fros_mk5'] = (0.0012*ros_df['ffdi']*fuel_load*1000).astype(int) #convert to m/h
    # ros_df['fros_mk5'].round(1)

    return ros_df

def ros_forest_vesta(
        df: DataFrame,
        fhs_surf: float,
        fhs_n_surf: float,
        fuel_height_ns: float, #cm
    ) -> DataFrame:
    """Forward Rate of Spread (FROS) from Project Vesta using fuel hazard 
    scores

    Eqn: 5.28

    Application: 
   
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


    # ros_df['mc'] = np.where(
    #     (ros_df['date_time'].dt.hour >= 9) & (ros_df['date_time'].dt.hour < 20),
    #     np.where(
    #         (ros_df['date_time'].dt.hour >= 12) & (ros_df['date_time'].dt.hour < 17), 
    #         2.76 + (0.124*ros_df['humidity']) - (0.0187*ros_df['temp']), 
    #         3.6 + (0.169*ros_df['humidity']) - (0.045*ros_df['temp'])
    #     ),
    #     3.08 + (0.198*ros_df['humidity']) - (0.0483*ros_df['temp'])
    # )
    if not 'mc' in ros_df.columns.values:
        ros_df['mc'] = get_mc(ros_df)

    # determine moisture function
    mf = 18.35 * ros_df['mc']**-1.495

    # determine the ROS
    ros_df['fros_vesta'] = np.where(
        ros_df['wind_speed'] > 5,
        30.0 + 1.531 * (ros_df['wind_speed']-5)**0.8576 * fhs_surf**0.93 * (fhs_n_surf*fuel_height_ns)**0.637 * 1.03,
        30
    )

    ros_df['fros_vesta'] = (ros_df['fros_vesta']* mf).astype(int)

    return ros_df

def ros_forest_vesta_fhr(
        df: DataFrame, 
        fhr_surf: str, 
        fhr_n_surf: str,
    ) -> DataFrame:
    """Forward Rate of Spread (FROS) from Project Vesta using fuel hazard
    ratings
    
    Eqn: 5.31

    Application: Wildfire in Sclerophyll (Eucalypt) forests
   
    Notes: anything else about the model.

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        fhr_surf: Surface Fuel Hazard Rating (L, M, H, V, E)
        fhr_n_surf: Near Surface Fuel Hazard Rating (L, M, H, V, E)

    Returns:
        a pandas dataframe including the fields
        
            `fros_vesta_fhr` the forward rate of spread (m/h)
    """
    ros_df = df.copy(deep=True)
    near_surface = {'L': 0.4694, 'M': 0.7070, 'H': 1.2772, 'V': 1.7492, 'E': 1.2446}
    surface = {'L': 0.0, 'M': 1.5608, 'H': 2.1412, 'V': 2.0548, 'E': 2.3251}

    surf_coeff = surface[fhr_surf]
    near_surf_coeff = near_surface[fhr_n_surf]

    if not 'mc' in ros_df.columns.values:
        ros_df['mc'] = get_mc(ros_df)

    # determine moisture function
    mf = 18.35 * ros_df['mc']**-1.495

    ros_df['fros_vesta_fhr'] = np.where(
        ros_df['wind_speed'] > 5,
        30.0 + 2.3117 * (ros_df['wind_speed']-5)**0.8364 * m.exp(surf_coeff+near_surf_coeff) * 1.02,
        30
    )
    ros_df['fros_vesta_fhr'] = (ros_df['fros_vesta_fhr']*mf).astype(int)

    return ros_df

def ros_grass(
    df: DataFrame, 
    state: str,
    curing: str,
):
    """Cheney et al. 1998 grass model.
    Eqns: 3.5, 3.6, 3.11

    Args:
        curing: Curing level (%)
        state: Grass state - natural (N), grazed (G), eaten out (E), (W) Woodlands, (F) Open forest
    """
    curing = max(20, curing)

    # create the ros dataframe from the datetime
    ros_df = df.copy(deep=True)
    
    # dead fuel moisture content from weather data Eqn 3.8
    ros_df['mc_g'] = 9.58 - 0.205*ros_df['temp'] + 0.138 * ros_df['humidity']
    
    # fuel moisture coeff Eqn 3.7
    ros_df['fm_coeff'] = np.where(
        ros_df['mc_g'] < 12,
        np.exp(-0.108*ros_df['mc_g']),
        np.where(
            ros_df['wind_speed'] < 10,
            0.684 - 0.0342*ros_df['mc_g'],
            0.547 - 0.0228*ros_df['mc_g']
        )
    )
    
    # curing coefficient from Eqn 3.10
    curing_coeff = 1.036/(1+103.99*m.exp(-0.0996*(curing-20)))

    #ros
    if state in 'NWF':
        # Eqn 3.5
        ros_df['fros_grass'] = np.where(
            ros_df['wind_speed'] > 5,
            (1.4 + 0.838*(ros_df['wind_speed'] - 5)**0.844)*ros_df['fm_coeff']*curing_coeff,
            (0.054 + 0.269*ros_df['wind_speed'])*ros_df['fm_coeff']*curing_coeff
        )

        if state == 'W':
             ros_df['fros_grass'] = ros_df['fros_grass'] * 0.5
        elif state == 'F':
            ros_df['fros_grass'] = ros_df['fros_grass'] * 0.3
        
    elif state in 'GE':
        # Eqn 3.6
        ros_df['fros_grass'] = np.where(
            ros_df['wind_speed'] > 5,
            (1.1 + 0.715*(ros_df['wind_speed'] - 5)**0.844)*ros_df['fm_coeff']*curing_coeff,
            (0.054 + 0.209*ros_df['wind_speed'])*ros_df['fm_coeff']*curing_coeff
        )
        if state == 'E':
            # Cruz et al. argue that should be half of G but no studies
            ros_df['fros_grass'] /= 2
        
    else:
        raise ValueError('Not a valid grass state')

    return ros_df

def ros_mallee(
    df: DataFrame,
    cover: int,
    height: float,
) -> DataFrame:
    """Cruz et al 2013 Semi-arid mallee heath.

    Eqns: 4.17, 4.18

    n = 61
    wind_speed range 5 - 28 km/h
    temp range 16 - 39 C
    humidity range 7 - 80 %
    total_fuel range 3.8 - 14.8 t/ha
    explains 0.74 of variability 

    Args:
        height: overstory height (m)
        cover: overstory cover (%)
    
    Returns:
        `DataFrame` including `fros_mallee`, `mc_m`

    """
    
    ros_df = df.copy(deep=True)

    #set delta = 1 if between 12:00 and 17:00 Sep-Mar, else 0
    ros_df['delta'] = 0
    ros_df['delta'] = ros_df['delta'].where(ros_df['date_time'].dt.month > 3, 1)
    ros_df['delta'] = ros_df['delta'].where(ros_df['date_time'].dt.month < 10, 1)
    ros_df['delta'] = ros_df['delta'].where(ros_df['date_time'].dt.hour > 11, 0)
    ros_df['delta'] = ros_df['delta'].where(ros_df['date_time'].dt.hour < 18, 0)
    
    ros_df['mc_m'] = (
        4.74 
        + 0.108*ros_df['humidity'] 
        - 0.1*(ros_df['temp'] - 25)
        - ros_df['delta']*(1.68+0.028*ros_df['humidity'])
        )
    ros_df['p_surface'] = (
        1 
        + np.exp(-(
            14.62+0.207*ros_df['wind_speed']
            -1.872*ros_df['mc_m']
            -0.304*cover
            ))
        )**-1
    ros_df['p_crown'] = (
        1 
        + np.exp(-(
            -11.138
            +1.4054*ros_df['wind_speed'] 
            - 3.4217*ros_df['mc_m']
            ))
        )**-1
    ros_df['fros_surface'] = (
        3.337
        *ros_df['wind_speed']
        *np.exp(-0.1284*ros_df['mc_m'])
        *height**-0.7073
        )
    ros_df['fros_crown'] = (
        9.5751
        *ros_df['wind_speed']
        *np.exp(-0.1795*ros_df['mc_m'])
        *(cover/100)**0.3589
        )
    # convert from m/min to km/h
    ros_df['fros_surface'] = ros_df['fros_surface']*0.06
    ros_df['fros_crown'] = ros_df['fros_crown']*0.06
    ros_df['fros_mallee'] = np.where(
        ros_df['p_surface'] < 0.5,
        0,
        (
            (1-ros_df['p_crown'])*ros_df['fros_surface']
            +ros_df['p_crown']*ros_df['fros_crown']
            )
    )
    return ros_df

########################################################################
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

    if `flank=True` the `ffdi` is calculated for a wind speed = 0

    Args:
        df: a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)
        wrf: a wind reduction factor
        flank: if `flank=True` the ffdi is calculated for a wind speed = 0
        DF: drought factor, this is only used if there is no `drought` in the 
            DataFrame

    Returns:
        a pandas Series of FFDI.
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
    
    return Series(ffdi.round(1))

def get_mc(df: DataFrame) -> Series:
    """Calculates the moisture content using equation 5.30

    Args:
        df (DataFrame): a pandas dataframe which must contain the specified the weather
            data. This can be an Incident dataframe (`Incident.df`)

    Returns:
        Series: the fine dead fuel moisture content (%)
    """

    mc = np.where(
        (df['date_time'].dt.hour >= 9) & (df['date_time'].dt.hour < 20),
        np.where(
            (df['date_time'].dt.hour >= 12) & (df['date_time'].dt.hour < 17), 
            2.76 + (0.124*df['humidity']) - (0.0187*df['temp']), 
            3.6 + (0.169*df['humidity']) - (0.045*df['temp'])
        ),
        3.08 + (0.198*df['humidity']) - (0.0483*df['temp'])
    )

    return Series(mc.round(1))



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