from src.pyropy.helpers import iwf_to_csv

iwf_fn = r"C:\Users\geoffg\Documents\Incidents\20221205_Stroud_Hill\NSW Special Fire Weather Forecast 13.html"
csv_fn = r"C:\Users\geoffg\Documents\Incidents\20221205_Stroud_Hill\20221205_Stroud_Hill_IWF.csv"
csv_fn = iwf_to_csv(iwf_fn, csv_fn)
