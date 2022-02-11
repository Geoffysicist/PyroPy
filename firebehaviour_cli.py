from src.firebehaviour import helpers as h
from src.firebehaviour import firebehaviour as fb
from src.firebehaviour import weather_data as wd
from openpyxl import Workbook, load_workbook

if __name__ == '__main__':
   weather_fn = 'tests/.data/weather_gridded_in.csv'
   weather_df = wd.gridded_to_df(weather_fn)
   incident = fb.Incident(weather_df)
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
   incident.run_forest_mk5()
   incident.run_forest_vesta()

   # fbcalc_fn = 'tests/.data/FireBehaviourCalcs_Test.xlsm'
   # wb = h.incident_to_calc(incident, fbcalc_fn)

   # wb.save('temp.xlsm')

   incident.print_head()
