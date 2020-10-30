import json

import pandas as pd

# In[]
# init api and load data

datfile = 'ampl/plant_location.dat'
satellites = pd.read_csv('satellites.csv')
stores = pd.read_csv('full_info.csv')
demand = pd.read_csv('fix_demand.csv')
with open('reference.json') as ref_file:
    ref = json.load(ref_file)

# In[]

# satellites = satellites.head(3)
stores = stores.head(7)
n = len(satellites)
m = len(stores)

with open(datfile, "w", encoding="utf-8") as file:
    file.write(f"set FACILITIES = {{1..{n}}};\n")
    file.write(f"set CUSTOMERS = {{1..{m}}};\n\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    file.write("param capacity :=\n")
    for i in range(n):
        file.write("%2d %5d\n" % (i+1, satellites['capacity'][i]))
    file.write(";\n\n")
# In[]

with open(datfile, "a", encoding="utf-8") as file:
    file.write("param demand :=\n")
    products_num = ref['products']["products_num"]
    week = [f"day-{i}" for i in range(1, 8)]
    for i in range(m):
        full_demand = 0.0
        for j in range(1, products_num+1):
            convert = ref["products"][f"product-{j}"]['in_m2']
            full_demand += sum(demand[week].loc[i*products_num+j]) / convert
        file.write("%2d %5f\n" % (i+1, full_demand))
    file.write(";\n\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    store_idxs = " ".join(map(str, [i for i in range(1, m + 1)]))
    file.write(f"param supplycost : {store_idxs} :=\n")
    with open('satelite_to_store.txt', "r", encoding="utf-8") as dist_file:
        i = 1
        for line in dist_file:
            file.write("%2d %s" % (i, line))
            i += 1
    file.write("\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    file.write(f"param fixcost : {store_idxs} :=\n")
    for i in range(n):
        file.write("%2d %5d\n" % (i+1, satellites['cost'][i]))
