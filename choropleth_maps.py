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
# plt.title("London Shapefile")
# map_df.plot()
# plt.show()

# pick relevant columns for visualization
df = data_df[[ 'Code',
              'Happiness_score_2011-14_(out_of_10)',
              'Population_density_(per_hectare)_2017',
              'Mortality_rate_from_causes_considered_preventable_2012/14']]

# rename columns to something simpler
data_for_map = df.rename(index=str, columns={'Happiness_score_2011–14_(out_of_10)': 'happiness',
                                                'Population_density_(per_hectare)_2017': 'pop_density_per_hectare',
                                                'Mortality_rate_from_causes_considered_preventable_2012/14': 'mortality'})
# View renamed dataframe
# chop of last 5 items in data_for_map to match the shape in map_df
data_for_map.drop(data_for_map.tail().index,inplace=True) # drop last n rows
print(data_for_map.shape)
print(map_df.shape)
# join dataset for mapping purposes
data_for_map["geometry"] = map_df["geometry"]
merged_dataset = data_for_map
print(merged_dataset.shape)
print(merged_dataset)

# map visualization
# set a variable that will call whatever column we want to visualise on the map
variable = 'pop_density_per_hectare'
# set the range for the choropleth
vmin, vmax = 120, 220
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))