import pandas as pd
from pandas import DataFrame
from pathlib import Path

def afdrs_meteograms_to_df(path) -> DataFrame:
    """"Creates a `DataFrame` from the indivudual csv downloads from
    AFDRS viewer metoegrams

    Writes the data to a `*.csv` file
    
    The output fields are:
    ```
    'date_time': 'Date time',
    'date': 'Date'
    'time': 'Time',
    'temp': 'Air temperature (°C)',
    'humidity': 'Relative humidity (%)',
    'wind_speed': '10 m wind speed (km/h)',
    'wind_dir': 'Wind direction (°)'
    ```
    
    Args:
    
    Returns:
        a pandas `DataFrame` with Amicus compatible fields
    """

    fields = {
        'date_time': 'Date time',
        'date': 'Date',
        'time': 'Time',
        'temp': 'Air temperature (°C)',
        'humidity': 'Relative humidity (%)',
        'wind_dir': 'Wind direction (°)',
        'wind_speed': '10 m wind speed (km/h)',
    }

    filenames = (
        'Relative Humidity.csv',
        'Wind Direction.csv',
        'Wind Speed.csv',
        'CHaines.csv',
        'Rate of Spread.csv',
        'Fire Intensity.csv',
        'Flame height.csv',
        'Fire Behaviour Index.csv',
        'Fire Danger Rating.csv',
        'Rubbish.csv',
    )

    df = pd.read_csv(path / 'Temperature.csv')
    
    for fn in filenames:
        this_path = path / fn
        if this_path.exists():
            _df = pd.read_csv(path / fn)
            df = df.merge(_df, how='inner')

    df['date'] = pd.to_datetime(df.date)
    date_local = df.date+pd.Timedelta(hours=11)
    df.insert(1,'Date',date_local.dt.date)
    df.insert(2,'Time',date_local.dt.time)
    df = df.rename(columns={'date':'DateTimeUTC'})
    
    fn = path / 'AFDRS_data.csv'
    df.to_csv(fn, index=False)
    #df['date'] = pd.to_datetime(df.date).tz_localize('Australia/Sydney')
    # df = df.datetime.to_frame()

    return df


if __name__ == '__main__':
    path = Path(r"C:\Users\geoffg\Documents\Incidents\20221203_Redhead\AFDRS_downloads")
    df = afdrs_meteograms_to_df(path)
    print(df.head())
