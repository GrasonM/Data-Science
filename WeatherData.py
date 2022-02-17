
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[5]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')



# In[11]:

from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.colors as mcol
import matplotlib.cm as cm
bin = 400
hash = 'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89'

Temp = pd.read_csv('data/C2A2_data/BinnedCsvs_d{}/{}.csv'.format(bin, hash))

Temp['Date'] = pd.to_datetime(Temp['Date'])

#Only doing this here because the mplleaflet in my personal jupyter notebook is bugged
#will take longer to execute, will take more lines of code for conversions and ultimately is less efficient than simply doing it with pandas. 
#print(datetime.strptime(Temp['Date'].to_json(), '%y-%m-%d')) = datetime.strptime(Temp['Date'], format)

Temp['Y'] = Temp['Date'].dt.year
Temp['M'] = Temp['Date'].dt.month
Temp['D'] = Temp['Date'].dt.day
Temp['DV'] = Temp['Data_Value'].div(10)
Temp['E'] = Temp['Element']

Temp = Temp[~((Temp['M']==2) & (Temp['D']==29))]
GrMin = Temp[(Temp['E']=='TMIN') & (Temp['Y']>=2005) & (Temp['Y']<2015)].groupby(['M','D']).agg({'DV':np.min})
FinMin = Temp[(Temp['E']=='TMIN') & (Temp['Y']==2015)].groupby(['M','D']).agg({'DV':np.min})
GrMax = Temp[(Temp['E']=='TMAX') & (Temp['Y']>=2005) & (Temp['Y']<2015)].groupby(['M','D']).agg({'DV':np.max})
FinMax = Temp[(Temp['E']=='TMAX') & (Temp['Y']==2015)].groupby(['M','D']).agg({'DV':np.max})

GrMax = GrMax.reset_index() 
GrMin = GrMin.reset_index() 
FinMax = FinMax.reset_index() 
FinMin = FinMin.reset_index() 

#x = GrMax
#y = GrMin
#X, Y = np.meshgrid(x,y)
#Z = f(X, Y)

AnomMin = FinMin[FinMin['DV'] < GrMin['DV']]
AnomMax = FinMax[FinMax['DV'] > GrMax['DV']]

#temps = range(-30,40)

plt.figure(figsize=(18, 10), dpi = 160)
red = '#FF0000'
blue = '#0800FF'
cm1 = mcol.LinearSegmentedColormap.from_list('Temperature Map',[blue, red])
cnorm = mcol.Normalize(vmin=min(GrMin['DV']),vmax=max(GrMax['DV']))
cpick = cm.ScalarMappable(norm=cnorm,cmap=cm1)
cpick.set_array([])
plt.title('Historical Temperature Analysis In Ann Arbor Michigan')
plt.xlabel('Month')
plt.ylabel('Temperature in Celsius')
plt.plot(GrMax['DV'], c = red, linestyle = '-', label = 'Highest Temperatures (2005-2014)')
plt.scatter(AnomMax.index, AnomMax['DV'], c = red, s=2, label = 'Anomolous High Readings (2015)')
plt.plot(GrMin['DV'], c = blue, linestyle = '-', label = 'Lowest Temperatures (2005-2014)')
plt.scatter(AnomMin.index, AnomMin['DV'], c = blue, s=2, label = 'Anomolous Low Readings (2015)')
plt.xticks(np.linspace(0,365,12, endpoint = True),(r'January',r'February',r'March',r'April',r'May',r'June',r'July',r'August',r'September',r'October',r'November',r'December'))

#Start: Assisted from StackOverFlow user JohanC v

x = np.arange(len(GrMin['DV'].fillna(0).astype('float64').ravel()))
y1 = GrMax['DV'].fillna(0).astype('float64').ravel()
y2 = GrMin['DV'].fillna(0).astype('float64').ravel()


polygon = plt.fill_between(x, y1, y2, lw=0, color='none')
xlim = (x.min(), x.max())
ylim = plt.ylim()
verts = np.vstack([p.vertices for p in polygon.get_paths()])
gradient = plt.imshow(np.linspace(1, 0, 256).reshape(-1, 1), cmap=cm1, aspect='auto',
                      extent=[verts[:, 0].min(), verts[:, 0].max(), verts[:, 1].min(), verts[:, 1].max()])
gradient.set_clip_path(polygon.get_paths()[0], transform=plt.gca().transData)
plt.xlim(xlim)
plt.ylim(ylim)

#Finish: Assisted from StackOverFlow user JohanC ^

#Failed Attempt at gradient fill with colormap
#plt.contourf(X, Y, Z, 20, cmap = cm1)
#for i in temps
#    plt.fill_between(len(GrMin['DV']), GrMin['DV'], i ,cmap = cm1)
#for i in temps
#    plt.fill_between(len(GrMin['DV']), i ,GrMax['DV'], cmap = cm1)

#Kind of Close but doesn't exactly create the colormap
#plt.gca().fill_between(range(len(GrMin.values)), GrMin['DV'], GrMax['DV'], facecolor = 'grey', alpha = 0.10)

plt.legend(loc = 'lower center', title='Temperature Guide')
plt.colorbar(cpick, label='Temperature in Celsius')
plt.show()


# In[ ]:



