#!/usr/bin/env python
# coding: utf-8

# In[103]:


import pandas as pd
import numpy as np


# In[104]:


def add_products(uni_param, a_days):
    tmp = []

    for i in range(a_days):
        tmp.append(round(np.random.normal(uni_param[0], uni_param[1])))
    return tmp


def create_demand_parameters(lb_avg_demand, ub_avg_demand, lb_dev, ub_dev):
    return [round(np.random.uniform(lb_avg_demand, ub_avg_demand)), round(np.random.uniform(lb_dev, ub_dev))]


# In[105]:


df = pd.read_csv('full_info.csv')

# In[106]:


df['key_adr'] = df['city'] + ' ' + df['street'] + ' ' + df['houseNumber']

# In[107]:


df = df.drop(columns=['countryCode', 'countryName', 'state', 'county', 'city', 'street', 'postalCode', 'houseNumber'])

# In[108]:


lb_avg_dem = [440, 50, 600, 170, 150, 15]
ub_avg_dem = [490, 60, 650, 180, 160, 25]
lb_d = [0, 0, 15, 3, 10, 0]
ub_d = [40, 10, 55, 5, 35, 5]
days = 7
products = 6

list_demand = []

for a in df['key_adr']:
    for p in range(products):
        t1 = [a, 'product-' + str(p + 1)]
        t2 = add_products(create_demand_parameters(lb_avg_dem[p], ub_avg_dem[p], lb_d[p], ub_d[p]), days)
        t1.extend(t2)
        list_demand.append(t1)

# In[109]:


headers = ['key_adr', 'product']

for i in range(days):
    headers.append('day-' + str(i + 1))

df_demand = pd.DataFrame(list_demand, columns=headers)

# In[110]:


num = df_demand._get_numeric_data()
num[num < 0] = 0

# In[111]:


df_demand = df_demand.set_index(['key_adr']).sort_index()

# In[112]:


df = df.set_index(['key_adr']).sort_index()

# In[113]:


total_demand = df_demand.join(df, on=['key_adr'])

# In[114]:


total_demand = total_demand.reset_index()

# In[115]:


total_demand = total_demand.set_index(['key_adr', 'product']).sort_index()

# In[116]:


print(total_demand.info())
print(total_demand.describe())

