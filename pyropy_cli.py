from src.pyropy import firebehaviour as fb
from src.pyropy import weather_data as wd

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
