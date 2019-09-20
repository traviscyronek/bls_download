"""
File:    bls_config.py
Author:  Travis Cyronek
Date:    6 February 2019
Purpose: Configuration for the bls downloader. Make sure you input your BLS
         API v2.0 key in the userSettings dictionary. If you do not already
         have a key, you can register for one at

             "https://data.bls.gov/registrationEngine/".

         In this file you'll be able to select where to save the data, what years
         are desired, and which series to download when the main file is run.
         The downloader works as follows. First, create a dictionary where the
         keys are BLS series IDs and the values are the variable name you want
         to assign to that series. The dictionary must have the following naming
         convention:

             "series_<SOURCE>_<DESCRIPTOR>".

         SOURCE is the source of the BLS data (e.g. laus, ces, oes, etc.) and
         DESCRIPTOR is some key identifier of what data are selected (e.g. the
         locations of the series you want to download). Next, you'll want to add
         this series to the userSettings dictionary as a key, where its value is
         a tuple of length 3 where the first value is in {0,1} and indicates
         whether you want to download that series when the the downloader is run
         and the second / third values are the desired start / end years to be
         extracted. When the main file is run, the appropriate series will be
         downloaded and saved to the <SOURCE>Dir directory as

             "<SOURCE>_<DESCRIPTOR>.csv".

         Note that it will be convenient to keep a record of the original name
         and units of these selected series for reference. As of writing, I am
         simply keeping track of these with comments next to the series below.
         If you want to run from the command line, simply type the following.

            "$ python 'path_to_file/bls_download.py'"
"""


# ----- user settings ----- #

userSettings = {
    # email and bls key
    'email': 'email@email.com',
    'blsKey': '123456789',
    # save directories
    'lausDir': '~/bls/laus/',
    'cesDir': '~/bls/ces/',
    'qcewDir': '~/bls/qcew/',
    # select which series to download and which years: ({0,1}, startYear, endYear)
    'series_laus': (0, 2000, 2018),
    'series_ces': (0, 2010, 2018),
    'series_qcew': (0, 2010, 2018)
}


# ----- example laus data ----- #

series_laus = {
    # 'California Metropolitan areas Santa Maria-Santa Barbara, CA Metropolitan Statistical Area Not Seasonally Adjusted'
    'LAUMT064220000000003': 'sb_lf',
    'LAUMT064220000000004': 'sb_emp',
    'LAUMT064220000000005': 'sb_unemp',
    'LAUMT064220000000006': 'sb_urate',    
    # 'California Statewide California Not Seasonally Adjusted'
    'LAUST060000000000003': 'ca_lf',
    'LAUST060000000000004': 'ca_emp',
    'LAUST060000000000005': 'ca_unemp',
    'LAUST060000000000006': 'ca_urate'
}


# ----- example ces industry employment data ----- #

series_ces = {
    # 'Not Seasonally Adjusted California Santa Maria-Santa Barbara, CA'
    'SMU06422000000000001': 'sb_indemp_0000000001', # 'Total Nonfarm All Employees, In Thousands'
    'SMU06422000500000001': 'sb_indemp_0500000001', # 'Total Private All Employees, In Thousands'
    'SMU06422000600000001': 'sb_indemp_0600000001', # 'Goods Producing All Employees, In Thousands'
    'SMU06422000700000001': 'sb_indemp_0700000001', # 'Service-Providing All Employees, In Thousands'
    'SMU06422000800000001': 'sb_indemp_0800000001', # 'Private Service Providing All Employees, In Thousands'
    'SMU06422001000000001': 'sb_indemp_1000000001', # 'Mining and Logging All Employees, In Thousands'
    'SMU06422001500000001': 'sb_indemp_1500000001', # 'Mining, Logging and Construction All Employees, In Thousands'
    'SMU06422002000000001': 'sb_indemp_2000000001', # 'Construction All Employees, In Thousands'
    'SMU06422003000000001': 'sb_indemp_3000000001', # 'Manufacturing All Employees, In Thousands'
    'SMU06422003100000001': 'sb_indemp_3100000001', # 'Durable Goods All Employees, In Thousands'
    'SMU06422004000000001': 'sb_indemp_4000000001', # 'Trade, Transportation, and Utilities All Employees, In Thousands'
    'SMU06422004100000001': 'sb_indemp_4100000001', # 'Wholesale Trade All Employees, In Thousands'
    'SMU06422004200000001': 'sb_indemp_4200000001', # 'Retail Trade All Employees, In Thousands'
    'SMU06422004244500001': 'sb_indemp_4244500001', # 'Food and Beverage Stores All Employees, In Thousands'
    'SMU06422004244800001': 'sb_indemp_4244800001', # 'Clothing and Clothing Accessories Stores All Employees, In Thousands'
    'SMU06422004300000001': 'sb_indemp_4300000001', # 'Transportation, Warehousing, and Utilities All Employees, In Thousands'
    'SMU06422005000000001': 'sb_indemp_5000000001', # 'Information All Employees, In Thousands'
    'SMU06422005500000001': 'sb_indemp_5500000001', # 'Financial Activities All Employees, In Thousands'
    'SMU06422005552000001': 'sb_indemp_5552000001', # 'Finance and Insurance All Employees, In Thousands'
    'SMU06422005553000001': 'sb_indemp_5553000001', # 'Real Estate and Rental and Leasing All Employees, In Thousands'
    'SMU06422006000000001': 'sb_indemp_6000000001', # 'Professional and Business Services All Employees, In Thousands'
    'SMU06422006054000001': 'sb_indemp_6054000001', # 'Professional, Scientific, and Technical Services All Employees, In Thousands'
    'SMU06422006055000001': 'sb_indemp_6055000001', # 'Management of Companies and Enterprises All Employees, In Thousands'
    'SMU06422006056000001': 'sb_indemp_6056000001', # 'Administrative and Support and Waste Management and Remediation Services All Employees, In Thousands'
    'SMU06422006500000001': 'sb_indemp_6500000001', # 'Education and Health Services All Employees, In Thousands'
    'SMU06422006561000001': 'sb_indemp_6561000001', # 'Educational Services All Employees, In Thousands'
    'SMU06422006562000001': 'sb_indemp_6562000001', # 'Health Care and Social Assistance All Employees, In Thousands'
    'SMU06422007000000001': 'sb_indemp_7000000001', # 'Leisure and Hospitality All Employees, In Thousands'
    'SMU06422007071000001': 'sb_indemp_7071000001', # 'Arts, Entertainment, and Recreation All Employees, In Thousands'
    'SMU06422007072000001': 'sb_indemp_7072000001', # 'Accommodation and Food Services All Employees, In Thousands'
    'SMU06422007072100001': 'sb_indemp_7072100001', # 'Accommodation All Employees, In Thousands'
    'SMU06422007072200001': 'sb_indemp_7072200001', # 'Food Services and Drinking Places All Employees, In Thousands'
    'SMU06422008000000001': 'sb_indemp_8000000001', # 'Other Services All Employees, In Thousands'
    'SMU06422009000000001': 'sb_indemp_9000000001', # 'Government All Employees, In Thousands'
    'SMU06422009091000001': 'sb_indemp_9091000001', # 'Federal Government All Employees, In Thousands'
    'SMU06422009091911001': 'sb_indemp_9091911001', # 'Department of Defense All Employees, In Thousands'
    'SMU06422009092000001': 'sb_indemp_9092000001', # 'State Government All Employees, In Thousands'
    'SMU06422009092161101': 'sb_indemp_9092161101', # 'State Government Educational Services All Employees, In Thousands'
    'SMU06422009092200001': 'sb_indemp_9092200001', # 'State Government Excluding Education All Employees, In Thousands'
    'SMU06422009093000001': 'sb_indemp_9093000001', # 'Local Government All Employees, In Thousands'
    'SMU06422009093161101': 'sb_indemp_9093161101', # 'Local Government Educational Services All Employees, In Thousands'
    'SMU06422009093200001': 'sb_indemp_9093200001', # 'Local Government excluding Educational Services All Employees, In Thousands'
}


# ----- example qcew data ----- #

series_qcew = {
    # 'Santa Barbara County, California Average Annual Pay All establishment sizes Private'
    'ENU0608350510': 'sb_avewage_all',        # 'Total, all industries'
    'ENU0608350511': 'sb_avewage_agri',       # 'NAICS 11 Agriculture, forestry, fishing and hunting'
    'ENU0608350521': 'sb_avewage_mining',     # 'NAICS 21 Mining, quarrying, and oil and gas extraction'
    'ENU0608350522': 'sb_avewage_util',       # 'NAICS 22 Utilities'
    'ENU0608350523': 'sb_avewage_const',      # 'NAICS 23 Construction'
    'ENU0608350531-33': 'sb_avewage_manuf',   # 'NAICS 31-33 Manufacturing'
    'ENU0608350542': 'sb_avewage_whole',      # 'NAICS 42 Wholesale trade'
    'ENU0608350544-45': 'sb_avewage_retail',  # 'NAICS 44-45 Retail trade'
    'ENU0608350548-49': 'sb_avewage_transp',  # 'NAICS 48-49 Transportation and warehousing'
    'ENU0608350551': 'sb_avewage_info',       # 'NAICS 51 Information'
    'ENU0608350552': 'sb_avewage_fin',        # 'NAICS 52 Finance and insurance'
    'ENU0608350553': 'sb_avewage_real',       # 'NAICS 53 Real estate and rental and leasing'
    'ENU0608350554': 'sb_avewage_proftech',   # 'NAICS 54 Professional and technical services'
    'ENU0608350556': 'sb_avewage_adminwaste', # 'NAICS 56 Administrative and waste services'
    'ENU0608350561': 'sb_avewage_educ',       # 'NAICS 61 Educational services'
    'ENU0608350562': 'sb_avewage_health',     # 'NAICS 62 Health care and social assistance'
    'ENU0608350571': 'sb_avewage_arts',       # 'NAICS 71 Arts, entertainment, and recreation'
    'ENU0608350572': 'sb_avewage_food',       # 'NAICS 72 Accommodation and food services'
    'ENU0608350581': 'sb_avewage_other'       # 'NAICS 81 Other services, except public administration'
}
