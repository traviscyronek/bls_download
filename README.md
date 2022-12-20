# bls_download
A python script for downloading public BLS data from its LABSTAT database. This is a wrapper for the BLS Public Data API v2.0 which handles some of the annoying constraints of the protocol. It hanldes the **request rate limit** of 50 requests per 10 sec, the **number of years to download limit** of 20 years, and the **number of series limi** of 50 series. There is additionally a 500 **daily query limit** to be aware of; the code will recognize that this limit is reached and print an error to the console. This code requires a registration key, which can be obtained at https://data.bls.gov/registrationEngine/.

## Usage
1. Change terminal directory to location of bls_download.py.
2. Update directory dictionary (in bls_download.py, the only thing in this file that should be edited by the user) with appropriate file locations.
3. Edit configuration file (a .json file where the important settings go, see example).
4. Execute the following in the terminal: "python bls_download.py --config=bls_config_example.json" or "python bls_download.py -c bls_config_example.json"
