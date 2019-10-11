import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

shapefile_path = 'data/London_Borough_Excluding_MHW.shx'
dataset_path = 'data/london-borough-profiles.csv'

#read data
map_df = gpd.read_file(shapefile_path)
map_df.reset_index(inplace=True)
data_df = pd.read_csv(dataset_path, header=0)

# view data
print(f'map dataframe from geopandas\n{map_df.head()}')
print(f'dataset entries \n{data_df.head()}')
# plt.title("London Shapefile")
map_df.plot()
plt.axis("off")
plt.show()

# pick relevant columns for visualization
df = data_df[[ 'Code',
               'Area_name',
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
data_for_map.reset_index(inplace=True)
# join dataset for mapping purposes
merged_dataset = map_df.join(data_for_map, lsuffix='l')
merged_dataset.drop(columns=['index','indexl'])

# map visualization
# set a variable that will call whatever column we want to visualise on the map
variable = 'pop_density_per_hectare'
color_map = "Greens"
# set the range for the choropleth
vmin, vmax = 120, 220
# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(10, 6))
# remove axes
ax.axis("off")
#plot map
merged_dataset.plot(column=variable, cmap=color_map, linewidth=0.9, ax=ax, edgecolor= '1.0')
# add a title
ax.set_title(variable, fontdict={'fontsize': '25', 'fontweight' : '3'})
# create an annotation for the data source
ax.annotate('Source: London Datastore, 2014',xy=(0.1, .08),
            xycoords='figure fraction', horizontalalignment='left',
            verticalalignment='top', fontsize=12, color='#555555')


# Add Labels
merged_dataset['coords'] = merged_dataset['geometry'].apply(lambda x: x.representative_point().coords[:])
merged_dataset['coords'] = [coords[0] for coords in merged_dataset['coords']]

for idx, row in merged_dataset.iterrows():
    plt.annotate(s=row['Area_name'], xy=row['coords'],horizontalalignment='right')

# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap=color_map, norm=plt.Normalize(vmin=vmin, vmax=vmax))
# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)
# if you wish for the colorbar to be horizontal
#fig.colorbar(sm, orientation="horizontal", fraction=0.036, pad=0.1, aspect = 30)
plt.show()
