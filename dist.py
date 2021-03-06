# In[]
import googlemaps
import numpy as np
import os
import pandas as pd
from pipenv.vendor import dotenv


# In[]
class Dist:
    def __init__(self, google_api_key):
        self.gmaps = googlemaps.Client(key=google_api_key)

    def get_dist(self, a, b, duration=True):
        directions = self.gmaps.directions(a, b)
        distance = 'distance'
        if duration:
            distance = 'duration'
        return directions[0]['legs'][0][distance]['value']


# In[]
# init api and load data
dotenv.load_dotenv(".env")

apikey = os.getenv('GOOGLE_API_KEY')
distApi = Dist(apikey)

stores = pd.read_csv('full_info.csv')
satellites = pd.read_csv('satellites.csv')
satellites_used = pd.read_csv('satellites_used.csv')
depots = pd.read_csv('depots.csv')

# stores = stores.head(7)
# satellites = satellites.head(3)
n = len(stores)
m = len(satellites)
mu = len(satellites_used)
l = len(depots)

# In[]
# get time between stores
time = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            a = str(stores['lat'][i]) + ", " + str(stores['lng'][i])
            b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
            time[i][j] = distApi.get_dist(a, b)
np.savetxt("time.txt", time, "%5d")


# In[]
# get distances between stores
dist = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            a = str(stores['lat'][i]) + ", " + str(stores['lng'][i])
            b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
            dist[i][j] = distApi.get_dist(a, b, duration=False)
np.savetxt("dist.txt", dist, "%6d")

# In[]
# get time between satelites and stores
time_sat_store = np.zeros((m, n))

for i in range(m):
    for j in range(n):
        a = satellites['location'][i]
        b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
        time_sat_store[i][j] = distApi.get_dist(a, b)
np.savetxt("satelite_to_store_time.txt", time_sat_store, "%5d")

# In[]
# get time between stores and satelites
time_sat_store = np.zeros((m, n))

for i in range(m):
    for j in range(n):
        a = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
        b = satellites['location'][i] 
        time_sat_store[i][j] = distApi.get_dist(a, b)
np.savetxt("store_to_satellite_time.txt", time_sat_store, "%5d")

# In[]
# get distances between satelites and stores
dist_sat_store = np.zeros((m, n))

for i in range(m):
    for j in range(n):
        a = satellites['location'][i]
        b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
        dist_sat_store[i][j] = distApi.get_dist(a, b, duration=False)
np.savetxt("satellite_to_store_dist.txt", dist_sat_store, "%5d")

# In[]
# get time and distances between stores and satellites
dist_store_sat = np.zeros((n, m))
time_store_sat = np.zeros((n, m))

for i in range(n):
    for j in range(m):
        a = str(stores['lat'][i]) + ", " + str(stores['lng'][i])
        b = satellites['location'][j]
        dist_store_sat[i][j] = distApi.get_dist(a, b, duration=False)
        time_store_sat[i][j] = distApi.get_dist(a, b, duration=True)
np.savetxt("store_to_satellite_dist.txt", dist_store_sat, "%6d")
np.savetxt("store_to_satellite_time.txt", time_store_sat, "%5d")

# In[]
# get time and distances between stores and satellites
dist_dep_satu = np.zeros((l, mu))
time_dep_satu = np.zeros((l, mu))

for i in range(l):
    for j in range(mu):
        a = depots['location'][i]
        b = satellites_used['location'][j]
        dist_dep_satu[i][j] = distApi.get_dist(a, b, duration=False)
        time_dep_satu[i][j] = distApi.get_dist(a, b, duration=True)
np.savetxt("dep_to_satellite_u_dist.txt", dist_dep_satu, "%6d")
np.savetxt("dep_to_satellite_u_time.txt", time_dep_satu, "%5d")

# In[]
# get distances between satelites and stores
dist_satu_store = np.zeros((mu, n))
time_satu_store = np.zeros((mu, n))

for i in range(mu):
    for j in range(n):
        a = satellites_used['location'][i]
        b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
        dist_satu_store[i][j] = distApi.get_dist(a, b, duration=False)
        time_satu_store[i][j] = distApi.get_dist(a, b, duration=True)
np.savetxt("satellite_u_to_store_dist.txt", dist_satu_store, "%5d")
np.savetxt("satellite_u_to_store_time.txt", dist_satu_store, "%5d")