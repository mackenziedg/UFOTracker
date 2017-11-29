from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import us

sns.set_style('whitegrid')

geo = pd.read_csv("../../data/raw/geocode.csv")
sightings = pd.read_csv("../../data/raw/ufo_sightings.csv")
sightings['loc'] = sightings.city + ", " + sightings.state

sightings = sightings.join(geo.set_index('loc'), on='loc')
sightings = sightings.dropna(subset=['lat'])
sightings = sightings[sightings.state.isin([st.abbr for st in us.states.STATES_CONTIGUOUS])]

# Limit the sightings to valid lat/long pairs in the contiguous USA
top = 49.3457868 # north lat
left = -124.7844079 # west long
right = -66.9513812 # east long
bottom = 24.7433195 # south lat
sightings = sightings[(sightings.lat.between(bottom, top))&(sightings.lon.between(left, right))]


m = Basemap(projection='merc', llcrnrlat=bottom, urcrnrlat=top, llcrnrlon=left, urcrnrlon=right, lat_ts=None, resolution='i')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.drawmapboundary(color='black')
lon, lat = m(sightings.lon.values, sightings.lat.values)

m.scatter(lon, lat, color='#174793', alpha=0.01)
plt.show()
