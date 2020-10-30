#!/usr/bin/env python
# coding: utf-8

# In[99]:


import pandas as pd
import numpy as np
import sklearn.cluster as cl
import matplotlib.pyplot as plt


# In[100]:


df = pd.read_csv('fix_demand.csv', encoding = 'utf-8')


# In[101]:


df_demand = df.drop(columns = ['day-2', 'day-3', 'day-4', 'day-5', 'day-6', 'day-7', 'lat', 'lng'])


# In[102]:


table_demand = pd.pivot_table(df_demand, values='day-1', index=['key_adr'], columns=['product'], aggfunc=np.sum)


# In[103]:


kmeans = cl.KMeans(n_clusters=7)


# In[104]:


kmeans.fit(table_demand)


# In[105]:


cl_dem_res = kmeans.labels_


# In[106]:


table_demand = table_demand.reset_index()


# In[107]:


tmp = pd.DataFrame(cl_dem_res, columns = ['cluster'])


# In[108]:


df_cl_d = table_demand.join(tmp)


# In[109]:


#df_cl_d.to_csv('cluster_by_demand.csv')


# In[110]:


df_position = df.drop(columns = ['product', 'day-1', 'day-2', 'day-3', 'day-4', 'day-5', 'day-6', 'day-7'])


# In[111]:


df_position = df_position.drop_duplicates(['key_adr', 'lat', 'lng']).reset_index(drop=True)


# In[112]:


df_position = df_position.set_index(['key_adr'])


# In[113]:


kmeans = cl.KMeans(n_clusters=7)


# In[114]:


kmeans.fit(df_position)


# In[115]:


cl_pos_res = kmeans.labels_


# In[116]:


cl_pos_centers = kmeans.cluster_centers_


# In[117]:


tmp1 = pd.DataFrame(cl_pos_res, columns = ['cluster'])
tmp2 = pd.DataFrame(cl_pos_centers, columns = ['c_lat', 'c_lng'])
tmp1 = tmp1.join(tmp2, on = 'cluster')


# In[118]:


df_position = df_position.reset_index()


# In[119]:


df_cl_p = df_position.join(tmp1)


# In[120]:


#df_cl_p.to_csv('cluster_by_position.csv')

