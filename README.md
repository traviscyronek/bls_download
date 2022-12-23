# bls_download
This is a repo for code that can be used to download various BLS data. Use whichever is appropriate, if any.

## labstat_download.py
A python script for downloading public BLS data from its LABSTAT database. This is a wrapper for the BLS Public Data API v2.0 which handles some of the annoying constraints of the protocol. It hanldes a *request rate limit* of 50 requests per 10 sec, a *number of years limit* of 20 years, and a *number of series limit* of 50 series. There is additionally a 500 *daily query limit* to be aware of; the code will recognize that this limit is reached and print an error to the console. This code requires a registration key, which can be obtained at https://data.bls.gov/registrationEngine/.

The particulars of what is downloaded, for what years, and where the output is saved is handled by .json configuration files. An example is given. Importantly this code works for public BLS series with a "Series ID." For more see https://www.bls.gov/help/hlpforma.htm.

### Usage
1. Change terminal directory to location of labstat_download.py.
2. Update directory dictionary (in labstat_download.py, the only thing in this file that should be edited by the user) with appropriate file locations.
3. Edit configuration file (a .json file where the important settings go, see example).
4. Execute the following in the terminal: "python labstat_download.py --config=labstat_config_example.json" or "python labstat_download.py -c labstat_config_example.json".

## cps_download.py
Downloads and renames monthly CPS basic monthly files from the NBER. Note that the first version is deprecated and no longer works. Please use cps_download_v2.py.

## qcew_download.py
Downloads selected QCEW files from https://www.bls.gov/cew/downloadable-data-files.htm.
