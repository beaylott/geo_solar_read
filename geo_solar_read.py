import pandas as pd
import numpy as np

import fnmatch
import os
from os.path import join

def read_geo_file(filename):
    data=pd.read_csv(filename,engine='python',header=0,skiprows=[0,1,2,3,5,6,7,8,9],index_col=0)
    data.index=pd.DatetimeIndex(data.index)
    data.index.name='Timestamp'
    return data[' Generated kWh']

def read_geo_files(folder):

    list_of_geo_filepaths=[]

    for root,dirs,files in os.walk(folder):
        for f in files:
            if fnmatch.fnmatch(f,'GEO*.DAT'):
                list_of_geo_filepaths.append(join(root,f))

    geo_data=[]

    if list_of_geo_filepaths:
        for geo_fp in list_of_geo_filepaths:
            geo_data.append(read_geo_file(geo_fp))

    return pd.concat(geo_data).sort_index()

def fix_solar_data(geo_data):

    last_datum=geo_data[0]
    offset=0.

    for i in geo_data.index:

        datum=geo_data[i]

        diff=datum-last_datum

        if diff<0.:
            offset=-diff

        geo_data[i]=datum+offset

        last_datum=datum

    return geo_data

def calculate_hourly_generation(geo_data):
    gd_h=geo_data.diff()
    gd_h[0]=geo_data[0]

def create_shef_solar_csv(geo_data,URN):
    gd=geo_data
    ss=pd.DataFrame(np.array([np.repeat(URN,geo_data.index.shape),gd.index.date,gd.index.time,gd.values.ravel()]).T)
    ss.to_csv('./test.csv',header=False,index=False)
