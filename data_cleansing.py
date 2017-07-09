
# coding: utf-8

# # Dashride Data Exploration

# ## 1. Data Extraction and cleansing

# In[1]:

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import timeit


# In[10]:

# load dataset into dataframe and filter out service level other than 'standard'
df = pd.read_csv('dataframe.csv', sep = ',', index_col = 0)
df = df[df['serviceLevel'] == 'standard']
df.head()


# In[17]:

# convert scheduledTime from string to datetime variable type and slice into weekdays
df['datetime'] = pd.to_datetime(df['scheduledTime'],format = '%Y-%m-%dT%H:%M:%S.000Z')
df['dayofweek'] = df['datetime'].dt.weekday_name
df.head()


# In[18]:

# save dataframe to csv file
df.to_csv('dataframe_cl.csv', sep = ',', index = False)


# In[ ]:



