from itertools import chain
from multiprocessing import Pool
import numpy as np
import pandas as pd
import re
from geopy.geocoders import GoogleV3
from time import sleep


def code_names(n):
    """Geocodes an array of placenames to longitudes and latitudes using Google Maps API.

    Parameters
    ----------
    n -- An array of place names as strings

    Returns
    -------
    lons -- An array of longitudes for each input place (None if that place failed to geocode properly)
    lats -- An array of latitudes for each input place (None if that place failed to geocode properly)
    """
    g = GoogleV3(api_key="AIzaSyC8AudJMjThy44TnVdsM195imL4XboSpng")

    lats, lons = [], []
    failed = []
    for ix, place in enumerate(n):
        try:
            loc = g.geocode(place, timeout=10)
            lats.append(loc.latitude)
            lons.append(loc.longitude)
        except:
            lats.append(None)
            lons.append(None)
            print('x', end='', flush=True)
            continue

        if ix % 100 == 0:
            print(ix, end='', flush=True)
        elif ix % 10 == 0:
            print('.', end='', flush=True)

    return lons, lats


# Read in only data from and after 1974
df = pd.read_csv("../../data/raw/ufo_sightings.csv")
df = df[df.index < 109088]

# Combine city, state pairs and remove duplicates
unique_locs = df.city + ", " + df.state
unique_locs = list(unique_locs.unique())

# Remove non-existant or malformed locations (includes all Canadian locations)
unique_locs = [i for i in unique_locs if type(i) is not float]
unique_locs = [i for i in unique_locs if re.match(r"^[0-9A-z ,.]+$", i)]

# Apply the geocoding to each subset of the unique_locs
n_workers = 30
p = Pool(n_workers)

ranges = list(range(0, len(unique_locs), int(len(unique_locs)/n_workers)))
ranges[-1] = len(unique_locs)
ranges = [(v, ranges[i+1]) for i, v in enumerate(ranges[:-1])]

# Outputs a `n_workers`-length array of sets of (lat, lon) tuples
out = p.map(code_names, [unique_locs[i[0]:i[1]] for i in ranges])

# Restructure the lats and lons
lats = [i[0] for i in out]
lons = [i[1] for i in out]
lats = list(chain.from_iterable(lats))
lons = list(chain.from_iterable(lons))

# Write to file
df = pd.DataFrame({'loc': unique_locs, 'lat': lats, 'lon': lons})
df = df.dropna()
df.to_csv("../../data/raw/geocode.csv", index=None)
