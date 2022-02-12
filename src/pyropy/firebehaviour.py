from dataclasses import dataclass
import warnings
from pandas import DataFrame

if __name__ == '__main__':
    import spreadmodels as fs
else:
    from . import spreadmodels as fs

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

class Incident(object):
    def __init__(self, weather_df: DataFrame):
        self.df = weather_df
        self.wrf = None
        self.fuel_load = None #t/ha
        self.fhs_surf = None
        self.fhs_n_surf = None 
        self.fuel_height_ns = None

        self.params = {
            'wrf': self.wrf,
            'fuel_load': self.fuel_load,
        }

    def get_params(self):
        return self.params


    def get_df(self):
        return self.df

    def update_params(self, params: dict) -> None:
        for key, val in params.items():
            setattr(self, key, val)
            self.params[key] = val

    def run_forest_mk5(self) -> None:
        forest_mk5_params = {
            'wrf': self.wrf,
            'fuel_load': self.fuel_load,
        }
        if self.check_params(forest_mk5_params):
            self.df = fs.ros_forest_mk5(self.df, self.wrf, self.fuel_load)

    def run_forest_vesta(self) -> None:
        forest_vesta_params = {
            'fhs_surf': self.fhs_surf,
            'fhs_n_surf': self.fhs_n_surf,
            'fuel_height_ns': self.fuel_height_ns,
        }

        if self.check_params(forest_vesta_params):
            self.df = fs.ros_forest_vesta(
                self.df, 
                self.fhs_surf, 
                self.fhs_n_surf, 
                self.fuel_height_ns,
            )

    def print(self, head=False):
        if head: print(self.df.head())
        else: print(self.df)

    def check_params(self, params) -> bool:
        for key, val in params.items():
            if not val:
                warnings.warn(f'{key} not set - run update params')
                return False
        return True

if __name__ == '__main__':
    pass