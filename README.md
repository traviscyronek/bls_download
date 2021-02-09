## bls_download

This script downloads selected series from various BLS programs using the BLS API v2.0. In order to work, you'll need to register a "key" which can be done at the following link.

    https://data.bls.gov/registrationEngine/

You'll need to input your institution, email address, and indicate that you've read and agree to the terms of service. An API key will then be promptly emailed to you. Note that there is a daily limit to the number of queries one can make with this key each day. The script is set up to download in groupings of series that I refer to as "batches." For example, one may construct a batch to include several series from the LAUS program, though these series do not need to all be from the same program. The only constraint is that each series in a batch have data on the start and end dates, and that they have the same periodicity (monthly, quarterly, etc.).

Each batch is defined by a dictionary object stored in bls_config.py. It must have "batch" in the name (e.g. "batch_laus"). It must also include entries specifying whether or not to download the batch, start and end dates, and save name and location. Most importantly, it should also include a nested dictionary of series which lists BLS series IDs as keys and desired variable names as values. For an example see the included configuration file. After running the script, any batches designated to be downloaded will be saved to the specified directory as "DATE_SAVENAME.csv".

You must know the series IDs in order to construct these batches. These IDs can be found across https://bls.gov. For more information on the structured naming convention, see 

https://www.bls.gov/help/hlpforma.htm.
