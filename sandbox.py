import shutil

from src.pyropy import weatherdata as ppw
from src.pyropy import firebehaviour as ppf
from src.pyropy import spreadmodels as pps
# weather = ppw.gridded_to_df('tests/.data/weather_gridded_in.csv')
# incident = ppf.Incident(weather)
# incident.thin_by_timestep(time_step=2)
# incident.trim_by_datetime('20211219 12:00', '20211220 23:59')
# pd = {0: ['drought']}
# incident.adjust_precision(pd)
# incident.print()

weather = ppw.gridded_to_df('tests/.data/Loch_Lamond2112.csv')
incident = ppf.Incident(weather)
incident.compare_fbcalc('tests/.data/lach_lamond_fbcalc.xlsm',['vesta2'])
