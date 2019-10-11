import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path = 'data/London_Borough_Excluding_MHW.shp'
dataset_path = 'data/london-borough-profiles.csv'

#read data
map_df = gpd.read_file(shapefile_path)
data_df = pd.read_csv(dataset_path, header=0)
# view data
print(f'map dataframe from geopandas{map_df.head()}')
print(f'dataset entries {data_df.head()}')
map_df.plot()
plt.show()