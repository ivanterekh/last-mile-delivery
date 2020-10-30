#!/usr/bin/env python
# coding: utf-8

# In[57]:


import pandas as pd
import numpy as np
import requests as r


# In[45]:


df_c = pd.read_csv('cluster_by_position.csv', index_col=0)


# In[46]:


df_s = pd.read_csv('satellites.csv')


# In[49]:


df_c['location'] = [str(x) + ',' + str(y) for x, y in zip(df_c['lat'], df_c['lng'])]
df_c['c_location'] = [str(x) + ',' + str(y) for x, y in zip(df_c['c_lat'], df_c['c_lng'])]
df_c = df_c.drop(columns = ['key_adr', 'lat', 'lng', 'c_lat', 'c_lng'])


# In[52]:


df_s = df_s.drop(columns = ['link', 'capacity', 'cost'])


# In[54]:


df_s['location'] = [x.replace(' ', '') for x in df_s['location']]


# In[113]:


poi_c =  df_c['location'].str.cat(sep=',')
poi_s = df_s['location'].str.cat(sep=',')
poi_ce = df_c['c_location'].str.cat(sep=',')


# In[114]:


api = 'bOZAeO552D42cNgIwLvUz0gVvU-JNWTFI9gmIXDL1qY'


# In[115]:


url_base = 'https://image.maps.ls.hereapi.com/mia/1.6/mapview?'
url_param = 'poi=' + poi_c + '&w=1280&h=900&apiKey=' + api
url = url_base + url_param


# In[116]:


response = r.get(url)


# In[117]:


response


# In[118]:


file = open("customers.png", "wb")
file.write(response.content)
file.close()


# In[119]:


url_base = 'https://image.maps.ls.hereapi.com/mia/1.6/mapview?'
url_param = 'poi=' + poi_s + '&w=1280&h=900&apiKey=' + api
url = url_base + url_param


# In[120]:


response = r.get(url)


# In[121]:


response


# In[122]:


file = open("satellites.png", "wb")
file.write(response.content)
file.close()


# In[123]:


url_base = 'https://image.maps.ls.hereapi.com/mia/1.6/mapview?'
url_param = 'poi=' + poi_ce + '&w=1280&h=900&apiKey=' + api
url = url_base + url_param


# In[124]:


response = r.get(url)


# In[125]:


response


# In[126]:


file = open("cl_centers.png", "wb")
file.write(response.content)
file.close()

