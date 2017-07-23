
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[3]:

df = pd.read_csv('new_dataframe_withInanHour.csv', sep = ',', index_col = 0)
df.head()


# In[4]:

df['waitingTime'].describe()


# In[5]:

# transform the date time columns data type from string to datetime
df['reservationTime'] = pd.to_datetime(df['reservationTime'],format = '%Y-%m-%dT%H:%M:%S')
df['rideStartedTime'] = pd.to_datetime(df['rideStartedTime'],format = '%Y-%m-%dT%H:%M:%S')
df['rideEndTime'] = pd.to_datetime(df['rideEndTime'],format = '%Y-%m-%dT%H:%M:%S')
df.head()


# In[6]:

df[['start_lt', 'start_lg', 'end_lt', 'end_lg']] = df[['start_lt', 'start_lg', 'end_lt', 'end_lg']].apply(lambda x: np.floor(x*100)/100)
df.head()


# In[8]:

df['hourofday'] = df['reservationTime'].dt.hour
df['dayofweek'] = df['reservationTime'].dt.weekday_name
df.head()


# In[9]:

df['startLoc'] = df['start_lg'].astype(str) + ', ' + df['start_lt'].astype(str)
df['endLoc'] = df['end_lg'].astype(str) + ', ' + df['end_lt'].astype(str)


# In[43]:

df_start_cluster = df[['dayofweek', 'hourofday','reservationNumber','startLoc']].groupby(['dayofweek','hourofday','startLoc']).nunique()
df_start_cluster.head()


# In[44]:

df_start_cluster['reservationNumber'].describe()


# In[45]:

df_start_cluster = df_start_cluster[df_start_cluster['reservationNumber'] >= 5]
df_start_cluster['reservationNumber'].describe()


# In[46]:

df_start_cluster.drop(['dayofweek','hourofday','startLoc'], axis = 1, inplace = True)
df_start_cluster.head()


# In[52]:

df_start_cluster.rename(columns = {'reservationNumber':'rideCount'}, inplace = True)
df_start_cluster.sort_index(level = [0,1], ascending = [True,True] , inplace = True)
df_start_cluster.head()


# In[76]:

df_start_cluster = df_start_cluster.merge(df[['startLoc','dayofweek','hourofday','start_lt','start_lg']], how = 'left', left_index = True, right_on = ['dayofweek','hourofday','startLoc']).reset_index(drop = True)
df_start_cluster.head()


# In[66]:

df_end_cluster = df[['dayofweek', 'hourofday','reservationNumber','endLoc']].groupby(['dayofweek','hourofday','endLoc']).nunique()
df_end_cluster.head()


# In[67]:

df_end_cluster['reservationNumber'].describe()


# In[69]:

df_end_cluster = df_end_cluster[df_end_cluster['reservationNumber'] >= 5]
df_end_cluster['reservationNumber'].describe()


# In[70]:

df_end_cluster.drop(['dayofweek','hourofday','endLoc'], axis = 1, inplace = True)
df_end_cluster.head()


# In[71]:

df_end_cluster.rename(columns = {'reservationNumber':'rideCount'}, inplace = True)
df_end_cluster.sort_index(level = [0,1], ascending = [True,True] , inplace = True)
df_end_cluster.head()


# In[74]:

df_end_cluster = df_end_cluster.merge(df[['endLoc','dayofweek','hourofday','end_lt','end_lg']], how = 'left', left_index = True, right_on = ['dayofweek','hourofday','endLoc']).reset_index(drop = True)


# In[75]:

df_end_cluster.head()


# In[77]:

df_start_cluster.to_csv('start_cluster.csv', sep = ',', index = False)


# In[78]:

df_end_cluster.to_csv('end_cluster.csv', sep = ',', index = False)


# In[ ]:



