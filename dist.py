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

stores = stores.head(7)
# satellites = satellites.head(3)
n = len(stores)
m = len(satellites)

# In[]
# get distances between stores
dist = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            a = str(stores['lat'][i]) + ", " + str(stores['lng'][i])
            b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
            dist[i][j] = distApi.get_dist(a, b)
print(dist)

# In[]
np.savetxt("dist.txt", dist, "%5d")

# In[]
# get distances between stores and satelites
distSatStr = np.zeros((m, n))

for i in range(m):
    for j in range(n):
        a = satellites['location'][i]
        b = str(stores['lat'][j]) + ", " + str(stores['lng'][j])
        distSatStr[i][j] = distApi.get_dist(a, b)
np.savetxt("satelite_to_store.txt", distSatStr, "%5d")
