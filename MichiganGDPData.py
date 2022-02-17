#!/usr/bin/env python
# coding: utf-8

# In[17]:


#Before trying this code, you will need to follow the instructions here -- https://medium.com/analytics-vidhya/fastest-way-to-install-geopandas-in-jupyter-notebook-on-windows-8f734e11fa2b
#you'll need a gcp account with google geolocation API and your own Client key for the below to work. The key below is mapped to my IP
#This is very much incomplete as I wanted to include the entire united states and add a fade effect. Almost like using a microscope and the only way to
#see the information is by zooming in closer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import googlemaps
import geopandas as gpd
import googlemaps 
from ipywidgets import widgets, interact



get_ipython().run_line_magic('matplotlib', 'notebook')
 
pd.set_option('display.max_rows', None)
cdat = pd.read_excel('Data/CountyMetro/AllData.xlsx', usecols ='B:C,E,G:AB').iloc[:-28,:]
cdat = cdat[cdat['LineCode']==3]
cdat = cdat.drop(cdat.columns[[1,2,3,4]], axis=1).reset_index(drop=True)
cdat['GeoName'] = cdat['GeoName'].str.replace(',', '').str.replace('Independent City','').str.replace(r'\([^)]*\)','').str.replace('(\*)', '')
cdat.set_index('GeoName',inplace = True)
#cdat
#cnames = list(dict.fromkeys(cdat.index))
#geo = pd.DataFrame()
#geo['Location'] = county_names
#geo['lat'] = ""
#geo['long'] = ""
#gm = googlemaps.Client(key = 'AIzaSyB721bHqnPxbCk5c4HpWq8lde4OiY72v5k')
#for x in range(len(geo)): 
    #try:
        #print('Fetching data ' + geo['Location'][x] )
        #result = gm.geocode(geo['Location'][x])
        #geo['lat'][x] = result[0]['geometry']['location']['lat']
       # geo['long'][x] = result[0]['geometry']['location']['lng']
     #   print('Data Fetched')
    #except IndexError:
       # print('Invalid Address')
#geo_data.to_csv('Data/StateCounty/scgeodata.csv')

gdp = pd.read_excel('Data/CountyMetro/AllData.xlsx', usecols ='B:C,E,G:AB').iloc[:-28,:]
gdp = gdp[gdp['LineCode']==3]
gdp = gdp.drop(gdp.columns[[1,2,3,4]], axis=1).reset_index(drop=True)
gdp['GeoName'] = gdp['GeoName'].str.replace(',', '').str.replace('Independent City','').str.replace(r'\([^)]*\)','').str.replace('(\*)', '')
locdat = pd.read_csv('Data/StateCounty/scgeodata.csv')
locdat = locdat[['Location','lat','long']]
locdat.rename(columns = {'Location':'GeoName'},inplace = True)
locdat.fillna(0)
usdf = pd.merge( locdat, gdp, how = 'outer', on = 'GeoName')
usdf = get_data()
usdf = usdf[['GeoName','long','lat',2020]]
#df[2020] = df[2020].replace(np.nan, 0).astype('float64')
#df[2020] = "${:,.2f}".format(df[2020].values)
MIdf = usdf[usdf['GeoName'].str.contains(' MI')]
MIdf['GeoName'] = MIdf['GeoName'].str.replace(' MI', ' County')
usdf = usdf[usdf['GeoName'].str.contains('MI')==False].reset_index(drop=True)
usdf['GeoName'] = usdf['GeoName'].str.replace(r'\b\w{1,2}\b$','County').str.replace(' Borough ',' ').str.replace(' Census Area ',' ').str.replace(' Municipality ',' ').str.replace(' Municipality ',' ').str.replace(' City and Borough ',' ')
usdf = usdf.drop(labels=[0,1,69,104,120,196,255,320,329,333,335,403,563,568,613,716,809,909,1015,1136,1201,1218,1243,1258,1259,1347,1430,1546,1603,1697,1715,1726,1748,1782,1845,1946,2000,2089,2167,2204,2272,2278,2325,2392,2488,2743,2773,2788,2894,2934,2990,3063], axis = 0).reset_index(drop=True)
usdf = usdf.iloc[usdf['GeoName'].sort_values().index.values].reset_index(drop=True)
#df['GeoName'] = df['GeoName'].str.replace(r'\w','County')
usmap = gpd.read_file('Data/CountyMetro/county.geojson')
usmap = usmap[['NAME','STATEFP','geometry']]
usmap['NAME'] = usmap['NAME'] + ' County'
usmap = usmap.sort_values(['NAME']).reset_index(drop=True)
usmap = usmap.iloc[usmap['NAME'].sort_values().index.values]
usmap = usmap.rename(columns={'NAME':'GeoName'})
m = usmap[usmap['STATEFP']=='26']
us = usmap[usmap['STATEFP']!='26']
mgdp = m.set_index('GeoName').join(MIdf.set_index('GeoName')).reset_index()
usgdp = us.set_index('GeoName').join(usdf.set_index('GeoName')).reset_index()

fig, ax = plt.subplots(1,figsize = (12,8), dpi = 80)
ax.axis('on')
ax.set(xlim=(-181, -64), ylim=(17, 72))
ax.set_title('Michigan GDP County Data', fontsize = 15)

c1 = 'Greens'
c2 = 'Gray'
vmin, vmax = 0,MIdf[2020].max()
cpick = plt.cm.ScalarMappable(cmap = c1, norm = plt.Normalize (vmin = vmin, vmax = vmax))
cpick._A = []
#cbar = fig.colorbar(cpick, fraction=0.046, pad=0.01)
usgdp.plot(color=c2,edgecolor='1.0',linewidth=0.5,ax=ax)
mgdp.plot(cmap=c1, edgecolor = '0.8' ,linewidth=0.8, ax=ax)
fig = plt.gcf()
fig.set_size_inches(10, 15)
gdf = gpd.GeoDataFrame(
    MIdf, geometry = gpd.points_from_xy(MIdf.long, MIdf.lat)
    )
fig.tight_layout()

plt.scatter(MIdf['long'], MIdf['lat'], color='k' ,picker = 5,s = 2)
plt.scatter('83', '42.5', color='yellow',picker = 5,s = 5)
ax.plot(82.90, 42.58, 'y')
#ax.annotate('Ann Arbor', (83, 43), 'k')

for i, txt in enumerate(MIdf[2020]):
    ax.annotate(txt, (MIdf.long.iat[i]+0.05, MIdf.lat.iat[i]))


# In[ ]:




