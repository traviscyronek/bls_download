"""
File:    bls_download.py
Author:  Travis Cyronek
Date:    2022-12-20

Purpose: Download bls series from the public API v2. You will need a
         registration key, which can be obtained at
         https://data.bls.gov/registrationEngine/.  There are some constraints
         with the API to be aware of: (1) daily query limit = 500, (2) request
         rate limit = 50 per 10 sec, (3) years to download limit = 20, (4)
         number of series to download = 50. All of these are handled by the
         program except for the daily query limit. If this is reached an error
         will be printed to the console to let you know that the download has
         failed.

Usage:   (Step 1) Change terminal directory to location of bls_download.py.
         (Step 2) Update directory dictionary below with appropriate locations.
         (Step 3) Edit configuration file, see example.
         (Step 4) Execute the following in terminal,
             "python bls_download.py --config=bls_config_example.json" or
             "python bls_download.py -c bls_config_example.json".
"""


directories = {'config_files': 'C:/Users/Travis/Dropbox/data/programs/', # location of your bls_config json files
               'downloads': 'C:/Users/Travis/Downloads/'} # some local download directory so dropbox /
                                                          #     google drive doesn't screw with temp file cleanup


# ---------------------------------------- #
#                                          #
#       DO NOT CHANGE ANYTHING BELOW       #
#                                          #
# ---------------------------------------- #


import datetime
import getopt
import json
import numpy as np
import os
import pandas as pd
import requests
import sys
import time


def processed_check(data):
    if data['status'] == 'REQUEST_NOT_PROCESSED':
        result = False
        message = data['message'][0]
    elif data['status'] == 'REQUEST_FAILED_INVALID_PARAMETERS':
        result = False
        message = 'In last request, ' + data['message'][0]
    else:
        result = True
        message = '0'
    return (result, message)


def convert_to_df(data, config_f):
    df = pd.DataFrame(columns=['series_id', 'year', 'period', 'value', 'footnotes'])
    for series in data['Results']['series']:
        series_id = series['seriesID']
        for item in series['data']:
            row = {'series_id': series_id,
                   'year': item['year'],
                   'period': item['period'],
                   'value': item['value'],
                   'footnotes': item['footnotes']}
            df = pd.concat([df, pd.DataFrame(data=row)])
    df['series_name'] = df['series_id']
    df['series_name'] = df['series_name'].map(config_f['series'])
    df = df[['series_id', 'series_name', 'year', 'period', 'value', 'footnotes']]
    return df


def merge_chunks(N_chunks, download_loc, config_f, the_date):
    df = pd.read_csv('{}{}_{}_chunk1.csv'.format(directories['downloads'],
                                                 the_date,
                                                 config_f['save_name']))
    for i in range(1, N_chunks+1):
        temp = pd.read_csv('{}{}_{}_chunk{}.csv'.format(directories['downloads'],
                                                        the_date,
                                                        config_f['save_name'],
                                                        i))
        df = pd.concat([df, temp], ignore_index=True)
    return df


def cleanup(download_loc):
    for root, dirs, files in os.walk(download_loc):
        for name in files:
            if 'chunk' in name:
                os.remove(os.path.join(root, name))


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:', ['config='])
    except getopt.GetoptError as err:
            print(err)
            sys.exit(2)

    # read-in config file
    for o, a in opts:
        if o in ('-c', '--config'):
            with open(directories['config_files']+a) as f:
                config_f = json.load(f)
            print('Attempting to download data for "{}" request...'.format(config_f['save_name']))
    series     = list(config_f['series'].keys())
    year_start = config_f['year_start']
    year_end   = config_f['year_end']
    N_series   = len(series)
    N_years    = year_end - year_start

    # we'll need to chunk the data if the request is large
    limit_s  = 50 # hard-coded series limit
    limit_y  = 20 # hard-coded years limit
    if N_series > limit_s or N_years > limit_y:
        print('Large request, API v2.0 limit reached (> 50 series and/or > 20 years). Chunking...')
        N_chunks_s = int(np.floor(N_series/limit_s)) + 1
        N_chunks_y = int(np.floor(N_years/(limit_y+1)))
        N_chunks   = N_chunks_s*N_chunks_y

    # retrieve the data from bls
    url      = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    headers  = {'Content-type': 'application/json'}
    the_date = datetime.date.today().strftime('%Y%m%d')
    t0       = time.perf_counter()
    if N_chunks > 1:
        chunk_counter = 1
        for i in range(N_chunks_s):
            for j in range(N_chunks_y):
                print('Downloading chunk {}/{}...'.format(chunk_counter, N_chunks))
                if i < N_chunks_s - 1:
                    series_chunk = series[limit_s*i+1:limit_s*(i+1)+1]
                else:
                    series_chunk = series[limit_s*i+1:N_series+1]
                if j < N_chunks_y - 1:
                    year_chunk = ((limit_y+1)*j+j, (limit_y+1)*(j+1)+j)
                else:
                    year_chunk = ((limit_y+1)*j+j, N_years+1)
                request = json.dumps({'seriesid': series_chunk,
                                      'startyear': year_start + year_chunk[0],
                                      'endyear': year_start + year_chunk[1],
                                      'registrationkey': config_f['registration_key']})
                retrieve = requests.post(url, headers=headers, data=request)
                data     = json.loads(retrieve.text)
                time.sleep(.2) # this ensures that there are fewer than 50 requests per 10 seconds (one could lower)
                sys.stdout.flush() # this keeps the console from freezing after time.sleep()
                result, message = processed_check(data)
                if result == False:
                    print(message)
                    exit() # kill process if daily limit has been reached
                df = convert_to_df(data, config_f)
                df.to_csv('{}{}_{}_chunk{}.csv'.format(directories['downloads'],
                                                       the_date,
                                                       config_f['save_name'],
                                                       chunk_counter), index=False)
                chunk_counter += 1
        df = merge_chunks(N_chunks, directories['downloads'], config_f, the_date)
        cleanup(directories['downloads'])
    else:
        request = json.dumps({'seriesid': series,
                              'startyear': year_start,
                              'endyear': year_end,
                              'registrationkey': config_f['registration_key']})
        retrieve = requests.post(url, headers=headers, data=request)
        data     = json.loads(retrieve.text)
        result, message = processed_check(data)
        if result == False:
            print(message)
            exit() # kill process if daily limit has been reached
        df       = convert_to_df(data, config_f)
    df.to_csv('{}{}_{}.csv'.format(config_f['save_loc'],
                                   the_date,
                                   config_f['save_name']), index=False)
    t1 = time.perf_counter()

    print('Output saved to {} as {}_{}.csv'.format(config_f['save_loc'], the_date, config_f['save_name']))
    print('Total download time = {} seconds'.format(round(t1-t0, 2)))


if __name__ == '__main__':
    main()
