import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

print("\n\nPROJEKTNI ZADATAK 9 (GEO 1)\n####################")

# Loading data from .shp file (adm1 - opstine Srbije)
try:
	opstine_gdf = gpd.read_file("data/SRB_adm1.shp")
	print("Shapefile uspešno učitan.")
except:
	raise Exception("Cannot load data")

opstine_gdf.plot()
plt.show()