#!/usr/bin/env python
# coding: utf-8

# In[252]:


import pandas as pd
import numpy as np


# In[253]:


def add_products(uni_param, a_days):
    tmp = []
    
    for i in range(a_days):
        tmp.append(round(np.random.normal(uni_param[0], uni_param[1])))
    return tmp

def create_demand_parameters(lb_avg_demand, ub_avg_demand, lb_dev, ub_dev):
    return [round(np.random.uniform(lb_avg_demand, ub_avg_demand)), round(np.random.uniform(lb_dev, ub_dev))]


# In[254]:


df = pd.read_csv('full_info.csv', encoding = 'cp1251')


# In[255]:


df['key_adr'] = df['city'] + ' ' + df['street'] + ' ' + df['houseNumber']


# In[256]:


df = df.drop(columns=['countryCode', 'countryName', 'state', 'county', 'city', 'street', 'postalCode', 'houseNumber'])


# In[257]:


lb_avg_dem = [440, 50, 600, 170, 150, 15]
ub_avg_dem = [490, 60, 650, 180, 160, 25]
lb_d = [0, 0, 15, 3, 10, 0]
ub_d = [40, 10, 55, 5, 35, 5]
days = 7
products = 6

list_demand = []

for a in df['key_adr']:
    for p in range(products):
        t1 = [a, 'product-' + str(p+1)]
        t2 = add_products(create_demand_parameters(lb_avg_dem[p], ub_avg_dem[p], lb_d[p], ub_d[p]), days)
        t1.extend(t2)
        list_demand.append(t1)
    


# In[258]:


headers = ['key_adr', 'product']

for i in range(days):
    headers.append('day-' + str(i+1))

df_demand = pd.DataFrame(list_demand, columns = headers)


# In[259]:


num = df_demand._get_numeric_data()
num[num < 0] = 0


# In[260]:


df_demand = df_demand.set_index(['key_adr'])


# In[261]:


df = df.set_index(['key_adr'])


# In[262]:


total_demand = df_demand.join(df, on=['key_adr'])


# In[263]:


total_demand = total_demand.reset_index()


# In[264]:


total_demand = total_demand.set_index(['key_adr', 'product'])


# In[265]:


total_demand


# In[268]:


total_demand[~total_demand.index.duplicated()]


# In[ ]:


#total_demand.to_csv('fix_demand.csv')

