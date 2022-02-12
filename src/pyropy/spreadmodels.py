"""
Fire Spread Models. 
Unless otherwise indicated all equations numbers refer to:
Cruz et al. 2015.

agnostic to slope ATM. Use discretion when plotting.
note Cruz et al. for large fires slope effect negligible
"""
# TODO 
# add flame hight and intensity
# flank ROS from length to breadth ratio

import numpy as np
from pandas import DataFrame, Series

def ros_forest_mk5(
        df: DataFrame, 
        wrf: float, 
        fuel_load: float,
    ) -> DataFrame:
    """McArthur 1973a Mk5 Forest Fire Danger Meter

    Params
        wrf: wind reduction factor
        fuel_load: fine fule load t/ha

    TODO use leaflet 80 when FFDI < 12
    """
    # ros_df = weather_df['date_time'].to_frame(name='date_time')
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

def get_FFDI(weather_df: DataFrame, wind_red: int = 3, flank=False, DF=9) -> Series:
    """Calculates FFDI from Eqn 5.19.

    if flank calculates the ffdi with wind speed = 0
    """
    if flank:
        wind_speed = 0
    else:
        wind_speed = weather_df['wind_speed']

    if not ('drought' in weather_df.columns): weather_df['drought'] = DF

    ffdi = 2.0*np.exp(
        -0.450 + 0.987*np.log(weather_df['drought'])
        -0.0345*weather_df['humidity']
        +0.0338*weather_df['temp']
        +0.0234* wind_speed * 3 / wind_red #Tolhurst wind reduction
        )
    
    return np.round(ffdi, 1)
