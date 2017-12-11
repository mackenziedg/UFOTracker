import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.ndimage.filters import gaussian_filter
import seaborn as sns
import shapefile
from subprocess import call
import urllib3
import us

sns.set_style('whitegrid')

geo = pd.read_csv("../../data/raw/geocode.csv")
sightings = pd.read_csv("../../data/raw/ufo_sightings.csv")
sightings['loc'] = sightings.city + ", " + sightings.state

sightings = sightings.join(geo.set_index('loc'), on='loc')
sightings = sightings.dropna(subset=['lat'])
sightings = sightings[sightings.state.isin([st.abbr for st in us.states.STATES_CONTIGUOUS])]

# Limit the sightings to valid lat/long pairs in the contiguous USA
top = 50.3457868 # north lat
left = -125.7844079 # west long
right = -65.9513812 # east long
bottom = 23.7433195 # south lat
sightings = sightings[(sightings.lat.between(bottom, top))&(sightings.lon.between(left, right))]

# Now we check if all of the shapefiles are downloaded or not
shapefile_dir = "./shapefiles"
try:
    os.mkdir(shapefile_dir)
except:
    pass

if os.listdir(shapefile_dir) == []:
    shapefile_urls = [st.shapefile_urls('state') for st in us.STATES_CONTIGUOUS]
    http = urllib3.PoolManager()
    shapefiles = [http.request('GET', url).data for url in shapefile_urls]
    shapefile_names = [i.split('/')[-1] for i in shapefile_urls]
    for data in shapefiles:
        with open("temp_shapefile.zip", "wb") as f:
            f.write(data)
        call(["unzip", "temp_shapefile.zip", "-d", shapefile_dir])

fig = plt.figure(figsize=(20, 13))
ax = fig.gca()

for filename in shapefile_names:
    shape = shapefile.Reader(shapefile_dir + "/" + filename)
    shape = shape.shape(0).__geo_interface__
    points = shape['coordinates']
    # import pdb; pdb.set_trace()

    for sh in points:
        if type(sh) == list:
            x = [x for x, _ in sh[0]]
            y = [y for _, y in sh[0]]
        elif type(sh) == tuple:
            x = [x for x, _ in sh]
            y = [y for _, y in sh]
        ax.plot(x, y, color='black')

    print(filename)
H, x, y = np.histogram2d(sightings.lat, sightings.lon, bins=100, range=((bottom, top), (left, right)))
scale = 0.25  # Power 0 > scale >= 1 to compress the dynamic range of the map
sigma = 0.2  # Gaussian filter sigma (larger is more "blurred")
ax.contourf(y[:-1], x[:-1], gaussian_filter(np.power(H, scale), sigma=sigma), alpha=0.9, cmap=plt.cm.bone)
# So because we're scaling the output for visualization purposes, showing the actual values on the colorbar is useless since they're the n-th root of the true values. There doesn't seem to be a way to replace the ticks so I guess there's no scale :(
ax.grid(False)
ax.axis('off')
# ax.set_title('UFO Sightings in the USA since 1974\nAs reported to NUFORC')
plt.savefig('./ufo_density_plot.png', bbox_inches='tight', dpi=300)
plt.show()
