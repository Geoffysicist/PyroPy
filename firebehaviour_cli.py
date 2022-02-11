from src.firebehaviour import firebehaviour as fb
from src.firebehaviour import weather_data as wd

if __name__ == '__main__':
   fn = 'tests/.data/weather_gridded_in.csv'
   weather_df = wd.gridded_to_df(fn)
   incident = fb.Incident(weather_df)
   incident.print_head()
   print(incident.get_params())
   params = {
      'wrf': 3,
      'fuel_load': 15,
   }
   incident.update_params(params)
   print(incident.get_params())
   incident.run_forest_mk5()
   incident.print_head()
   params = {
      'fhs_surf': 3.5,
      'fhs_n_surf': 3,
      'fuel_height_ns': 20,
   }
   incident.update_params(params)
   incident.run_forest_vesta()
   incident.print_head()

   fn = 'tests/.data/weather_amicus_out.csv'
   # amicus_df = wd.df_to_amicus(incident.df, fn)
   