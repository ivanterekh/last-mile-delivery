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
dotenv.load_dotenv(".env")

apikey = os.getenv('GOOGLE_API_KEY')
distApi = Dist(apikey)

df = pd.read_csv('full_info.csv')

df = df.head(5)
n = len(df)

# In[]
dist = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        if i != j:
            a = str(df['lat'][i]) + ", " + str(df['lng'][i])
            b = str(df['lat'][j]) + ", " + str(df['lng'][j])
            dist[i][j] = distApi.get_dist(a, b)
print(dist)

# In[]
np.savetxt("dist.txt", dist, "%5d")
