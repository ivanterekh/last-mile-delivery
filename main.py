import googlemaps
import numpy as np
import os
from pipenv.vendor import dotenv


def main():
    dotenv.load_dotenv(".env")

    apikey = os.getenv('GOOGLE_API_KEY')
    gmaps = googlemaps.Client(key=apikey)

    points = ['53.955144, 27.620091', '53.907657, 27.432110', '53.898782, 27.554962', '53.889792, 27.574859']

    n = len(points)
    dist = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                directions = gmaps.directions(points[i],
                                              points[j],
                                              mode="driving")
                # uncomment to use duration instead of distance
                # dist[i][j] = directions[0]['legs'][0]['duration']['value']
                dist[i][j] = directions[0]['legs'][0]['distance']['value']
    print(dist)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
