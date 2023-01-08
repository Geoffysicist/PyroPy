import src.pyropy.spreadmodels as pps
import src.pyropy.helpers as pph
import src.pyropy.weatherdata as ppw

def main():
    logger = pph.get_logger()

    logger.info(f'{logger.name}')

    fn = 'tests/.data/weather_gridded_in.csv'
    df = ppw.gridded_to_df(fn)
    df['FFDI'] = pps.get_FFDI(df.temp, df.humidity, df.wind_speed, df.drought, wrf = 3.5)

    logger.info(df.head())

if __name__ == '__main__':
    main()
