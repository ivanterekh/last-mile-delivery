import json

import pandas as pd

# In[]
# init api and load data

datfile = 'ampl/two_echelon_location.dat'
satellites = pd.read_csv('satellites_used.csv')
stores = pd.read_csv('full_info.csv')
depots = pd.read_csv('depots.csv')
demand = pd.read_csv('fix_demand.csv')
with open('reference.json') as ref_file:
    ref = json.load(ref_file)

# In[]

# satellites = satellites.head(3)
# stores = stores.head(7)
n = len(satellites)
m = len(stores)
l = len(depots)

with open(datfile, "w", encoding="utf-8") as file:
    file.write(f"param N = {n};\n")
    file.write(f"param M = {m};\n")
    file.write(f"param L = {l};\n\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    file.write("param capacity :=\n")
    for i in range(n):
        file.write("%2d %5d\n" % (i + 1, satellites['capacity'][i]))
    file.write(";\n\n")
# In[]

with open(datfile, "a", encoding="utf-8") as file:
    file.write("param demand :=\n")
    products_num = ref['products']["products_num"]
    week = [f"day-{i}" for i in range(1, 8)]
    for i in range(m):
        full_demand = 0.0
        for j in range(products_num):
            convert = ref["products"][f"product-{j+1}"]['in_m2']
            full_demand += sum(demand[week].loc[i * products_num + j]) / convert
        file.write("%2d %5f\n" % (i + 1, full_demand))
    file.write(";\n\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    store_idxs = " ".join(map(str, [i+1 for i in range(m)]))
    file.write(f"param dist_from_sat : {store_idxs} :=\n")
    with open('satellite_u_to_store_time.txt', "r", encoding="utf-8") as dist_file:
        i = 1
        for line in dist_file:
            file.write("%2d %s" % (i, line))
            i += 1
    file.write(";\n\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    satellite_idxs = " ".join(map(str, [i+1 for i in range(n)]))
    file.write(f"param dist_from_dep : {satellite_idxs} :=\n")
    with open('dep_to_satellite_u_time.txt', "r", encoding="utf-8") as dist_file:
        i = 1
        for line in dist_file:
            file.write("%2d %s" % (i, line))
            i += 1
    file.write(";\n\n")

# In[]

with open(datfile, "a", encoding="utf-8") as file:
    file.write(f"param cost_dep :=\n")
    for i in range(l):
        file.write("%2d %5d\n" % (i + 1, depots['cost'][i]))
    file.write(";\n\n")

# In[12]

with open(datfile, "a", encoding="utf-8") as file:
    file.write("param cost_from_sat = 12;\n")
    file.write("param cost_from_dep = 20;\n")
