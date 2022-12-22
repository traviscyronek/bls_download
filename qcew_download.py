"""
File:    qcew_download.py
Author:  Travis Cyronek
Purpose: Downloads selected QCEW files from
         https://www.bls.gov/cew/downloadable-data-files.htm
"""

layout   = 'qtrly_singlefile'
save_loc = 'C:/Users/Travis/Dropbox/data/bls/qcew/'


# ---------------------------------------- #
#                                          #
#       DO NOT CHANGE ANYTHING BELOW       #
#                                          #
# ---------------------------------------- #


from bs4 import BeautifulSoup
import os
import re
import requests


def downloader(layout, save_loc):

    """
    Description: downloads qcew files if not already downloaded in save_loc

    Inputs:
        layout   -- (str) one of 'qtrly_by_area', 'annual_by_area',
                          'qtrly_by_industry', 'annual_by_industry', 'qtrly_singlefile', or
                          'annual_singlefile'
        save_loc -- (str) directory to write to
    """

    url = 'https://www.bls.gov/cew/downloadable-data-files.htm'
    soup = BeautifulSoup(requests.get(url).content)
    links = soup.find_all('a', attrs={'href': re.compile('https://data.bls.gov/cew/data/files/')})
    links = soup.find_all('a', href=re.compile(layout))

    for link in links:
        href = link.get('href')
        file_name = href.split('/')[-1]
        if os.path.exists(save_loc+file_name):
            print(f'{href} already downloaded. Skipping...')
        else:
            print(f'Downloading {href}...')
            results = requests.get(href)
            with open(save_loc+file_name, 'wb') as f:
                f.write(results.content)

    print('Download Complete!')


if __name__ == '__main__':
    downloader(layout, save_loc)
