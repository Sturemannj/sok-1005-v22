#avokadopriser i usa 



#!/usr/bin/env python
# coding: utf-8

# In[19]:



#impoerterer pakker..
import numpy as np
import pandas as pd
import plotly.express as px 

#her har jeg funnet en basic og enkel pakke som heter plotly. denne er hovedpakken til resultatene


# In[22]:


#leser datasaett til dataframe 
df = pd.read_csv('avocado-updated-2020.csv')
df.info()
#her viser innholdet til priser 


# In[43]:


#plotter en tabell som data er oppsatt. 
avocado.head()


# In[24]:


#viser katogoriserte variabler. 
print(df['type'].value_counts(dropna=False))
print(df['geography'].value_counts(dropna=False)) 


# In[56]:


#her vises første polttet. her har jeg valgt New Yourk. men kan endes veldig nekelt ved å Endre på df['geography'] == 'HER'
msk = df['geography'] == 'New York'
px.line(df[msk], x='date', y='average_price', color='type')


# In[31]:


#Her lager jeg en Boxplot av Conventional and Organic Avocados
# der kan man se dyreste og billigste priser på Conventional and Organic Avocados. 
conventional_avocado = avocado[avocado['type']=='conventional']
organic_avocado = avocado[avocado['type']=='organic']

fig = make_subplots(rows=1, cols=2, subplot_titles=('Conventional Avocados',' Organic Avocados'))

trace1 = go.Box(y=conventional_avocado['average_price'],name ='Conventional Avocados')

trace2 = go.Box(y=organic_avocado['average_price'], name ='Organic Avocados')

fig.append_trace(trace1, row = 1, col=1)
fig.append_trace(trace2, row = 1, col=2)
fig.show()
