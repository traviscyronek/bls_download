"""
File:    bls_download.py
Author:  Travis Cyronek
Date:    7 February 2019
Purpose: This script downloads selected series from the BLS using the BLS API
         v2.0. In order to work, you'll need to register a "key" which can be
         done at the following link.

             https://data.bls.gov/registrationEngine/

         Note that there is a daily limit to the number of queries one can make
         with this key each day, though you shouldn't ever really reach this
         limit. The only thing that should be touched in this file is setting
         the working directory to the bls scripts folder. All other settings are
         handled in config.py.
"""

pwd = '~/bls/'


# ------------------- #
#                     #
#       Imports       #
#                     #
# ------------------- #

import datetime
import json
import os
import pandas as pd
import requests
os.chdir(pwd)
import bls_config


# --------------------- #
#                       #
#       Functions       #
#                       #
# --------------------- #

def bls_download(series, startYear, endYear, blsKey, saveDir, saveName):

    # ----- request the data from the bls website ----- #

    url     = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'                                 # api url
    headers = {'Content-type': 'application/json'}                                                # specify json as the content type to return
    data    = json.dumps({"seriesid": list(series.keys()), "startyear": startYear, "endyear": endYear}) # submit the list of series as data
    p       = requests.post('{}{}'.format(url, blsKey), headers=headers, data=data).json()['Results']['series'] # post request for the data


    # ----- convert to pandas dataframe and save ----- #

    dateList = [f"{i['year']}-{i['period'][1:]}-01" for i in p[0]['data']] # date index from first series
    df = pd.DataFrame()                                                    # empty dataframe to fill with values
    for s in p:                                                            # build a pandas series from the results
        df[series[s['seriesID']]] = pd.Series(index = pd.to_datetime(dateList), data = [i['value'] for i in s['data']]).astype(float).iloc[::-1]
    theDate = datetime.date.today().strftime('%Y%m%d')                     # find today's date to put in filename
    df.to_csv(saveDir+theDate+saveName)                                    # save to file
    print('Finished downloading "{}"'.format(theDate+saveName)+' to "{}"'.format(saveDir))


# -------------------- #
#                      #
#       Download       #
#                      #
# -------------------- #

if __name__ == '__main__':
    batchList = [item for item in dir(config) if 'series' in item] # find all of the series dictionaries in the configuration file
    for batch in batchList:
        dlBatch = config.userSettings[batch][0]
        if dlBatch == 1:
            bls_download(eval('config.'+batch),
                         eval('config.userSettings[\''+batch+'\'][1]'),
                         eval('config.userSettings[\''+batch+'\'][2]'),
                         '?registrationkey={}'.format(config.userSettings['blsKey']),
                         config.userSettings[batch.split('_')[1]+'Dir'],
                         batch.split('series')[1]+'.csv')
