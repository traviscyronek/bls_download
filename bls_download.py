"""
File:    bls_download.py
Author:  Travis Cyronek
Date:    7 February 2021
Purpose: Main file to download BLS series data. The only changes that should be
         made to this file are the config_loc and bls_key variables.
"""

# TODO: Currently the downloader breaks during the conversion to the pandas
#       dataframe format if the time series start (or end) at different
#       points in time. It would be nice to fix this at some point and just
#       leave empty cells if no data are there.


# ------------------------- #
#                           #
#       Preliminaries       #
#                           #
# ------------------------- #

# user settings
config_loc = '~/bls/scripts/'
bls_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'

# imports
import datetime
import json
import os
import pandas as pd
import requests
os.chdir(config_loc)
import bls_config


# --------------------- #
#                       #
#       Functions       #
#                       #
# --------------------- #

def bls_download(series, start_year, end_year, bls_key, save_dir, save_name):

    # request the data from the bls website
    url     = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    headers = {'Content-type': 'application/json'}
    data    = json.dumps({"seriesid": list(series.keys()), "startyear": start_year, "endyear": end_year})
    p       = requests.post('{}{}'.format(url, bls_key), headers=headers, data=data).json()['Results']['series']

    # convert to pandas dataframe and save
    date_list = [f"{i['year']}-{i['period'][1:]}-01" for i in p[0]['data']]
    df = pd.DataFrame()
    for s in p:
        df[series[s['seriesID']]] = pd.Series(index = pd.to_datetime(date_list),
            data = [i['value'] for i in s['data']]).astype(float).iloc[::-1]
    the_date = datetime.date.today().strftime('%Y%m%d')
    df.to_csv(save_dir+the_date+'_'+save_name)
    print('Finished downloading "{}"'.format(the_date+'_'+save_name)+' to "{}"'.format(save_dir))


# -------------------- #
#                      #
#       Download       #
#                      #
# -------------------- #

if __name__ == '__main__':
    batch_list = [item for item in dir(bls_config) if 'batch' in item]
    for batch in batch_list:
        if eval('bls_config.'+batch+'[\'download\']') == True:
            bls_download(eval('bls_config.'+batch+'[\'series\']'),
                         eval('bls_config.'+batch+'[\'start_year\']'),
                         eval('bls_config.'+batch+'[\'end_year\']'),
                         '?registrationkey={}'.format(bls_key),
                         eval('bls_config.'+batch+'[\'save_dir\']'),
                         eval('bls_config.'+batch+'[\'save_name\']')+'.csv')
