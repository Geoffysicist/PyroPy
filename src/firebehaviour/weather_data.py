"""Reading, transforming and writing weather data for fire behavior."""
import pandas as pd
from pandas import DataFrame

if __name__ == '__main__':
    from helpers import check_filepath, check_encoding
else:
    from .helpers import check_filepath, check_encoding

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

FIELDS_AMICUS = {
    'date_time': 'Date time',
    'temp': 'Air temperature (°C)',
    'humidity': 'Relative humidity (%)',
    'wind_speed': '10 m wind speed (km/h)',
    'wind_dir': 'Wind direction (°)' #TODO replace all degree symbols
}

def weather_to_df(
        fn: str,
        header: int = 0, 
        col_names: dict = FIELDS_BASE, 
        datetime_format: str = "%d/%m/%Y %H:%M",
    ) -> DataFrame:
    """reads weather obs into a pandas df
    Args:
        fn: the path to the csv or axf file
        header: the line containing the column headers
        col_names: the dictionary containing the column names. See README
        datetime_format: string format for the date times
    """
    check_filepath(fn, suffix='csv')
    #swap the keys and vals in the dictionary
    col_names = {y:x for x,y in col_names.items()}
    
    # avoid UnicodeDecodeError:
    df = pd.read_csv(fn, header=header, encoding=check_encoding(fn))
    
    df = df.rename(columns=col_names)

    #just want a single datetime column containing datetime objects
    if set(['date','time']).issubset(df.columns):
        df['date_time'] = df[["date", "time"]].agg(" ".join, axis = 1)
        df = df.drop(['date','time'], axis='columns')
    if 'date_time' in df.columns:
        if datetime_format:
            df['date_time'] = pd.to_datetime(df['date_time'],format=datetime_format)
        else:
            df['date_time'] = pd.to_datetime(df['date_time'],infer_datetime_format=True)
    
    #TODO if wind dir is str then change to degrees
    # if 'wind_dir_cp' in df.columns:
    #     df['wind_dir'] = df['wind_dir_cp'].apply(lambda cp : cardinal_to_degrees(cp))
    #     df = df.drop(['wind_dir_cp'], axis='columns')

    # remove unused column names from the base dict
    col_names = {key:val for key,val in FIELDS_BASE.items() if key in df.columns}

    return df[col_names.keys()]

def gridded_to_df(fn: str) -> DataFrame:
    return weather_to_df(fn, header = 6, col_names = FIELDS_GRIDDED, datetime_format="%d/%m/%Y %H:%M")

def df_to_weather(df: DataFrame, fn: str, col_names = FIELDS_BASE, datetime_format="%Y%m%d %H:%M", encoding=None) -> DataFrame:
    """" If datetime_format == 'iso8601' the output format will be %Y-%m-%dT%H:%M:%s+11:00
    """
    df = df.copy()
    if 'date' in col_names.keys():
        df['date'] = df['date_time'].dt.strftime(datetime_format.split()[0])
    if 'time' in col_names.keys():
        df['time'] = df['date_time'].dt.strftime(datetime_format.split()[1])

    if 'date_time' in col_names.keys():
        df['date_time'] = df['date_time'].dt.strftime(datetime_format)
        # df['date_time'] = df['date_time'].dt.strftime("%d/%m/%Y %H:%M")

    
    # remove unused column names from the base dict
    col_names = {key:val for key,val in col_names.items() if key in df.columns}
    df = df[col_names.keys()]
    df = df.rename(columns=col_names)
    
    df.to_csv(fn, index=False, encoding=encoding)
    return df

def df_to_amicus(df, fn: str) -> DataFrame:
    return df_to_weather(df, fn, col_names=FIELDS_AMICUS, datetime_format="%d/%m/%Y %H:%M", encoding='cp1252')

if __name__ == '__main__':
    pass
