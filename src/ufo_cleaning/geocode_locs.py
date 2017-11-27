import pandas as pd
import re
from geopy.geocoders import GoogleV3
from time import sleep

# Read in only data from and after 1974
df = pd.read_csv("../../data/raw/ufo_sightings.csv")
df = df[df.index < 109088]

# Combine city, state pairs and remove duplicates
unique_locs = df.city + ", " + df.state
unique_locs = list(unique_locs.unique())

# Remove non-existant or malformed locations (includes all Canadian locations)
unique_locs = [i for i in unique_locs if type(i) is not float]
unique_locs = [i for i in unique_locs if re.match(r"^[0-9A-z ,.]+$", i)]

# Geocodes each unique location
# Cuts down the number needed from >100k to ~20k
# Doing per item is maybe slower but allows to see where the
# script left off if it crashes
g = GoogleV3(api_key="no show")

lats, lons = [], []
failed = []
for ix, place in enumerate(unique_locs):
    try:
        loc = g.geocode(place, timeout=10)
    except:
        failed.append(ix)
        continue

    lats.append(loc.latitude)
    lons.append(loc.longitude)
    if ix % 100 == 0:
        print(ix)
    else:
        print('.', end='', flush=True)
    # sleep(0.1)

