import argparse
import requests
import pandas as pd

# refer to https://api.census.gov/data/2019/acs/acs1/variables.html get needed variable
# https://www.census.gov/data/developers/data-sets/acs-1year.2019.html#list-tab-843855098 for api capture info
# name: Name
# income
income = "B19013_001E"
# total population
poplation = "B01003_001E"
# education level population: 
edu_level = "B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E"
# Age group:
# Age population 15-24 (teen): [male]: 
male_teen = "B01001_006E,B01001_007E,B01001_008E,B01001_009E,B01001_010E"
# [female]: 
female_teen = "B01001_030E,B01001_031E,B01001_032E,B01001_033E,B01001_034E"
teen = male_teen + "," + female_teen
# Age population 25-34 (young): [male]: 
male_young = "B01001_011E,B01001_012E"
# [female]: 
female_young = "B01001_035E,B01001_036E"
young = male_young + "," + female_young
# Age population 35-54 (middle): [male]:
male_middle = "B01001_013E,B01001_014E,B01001_015E,B01001_016E"
# [female]: 
female_middle = "B01001_037E,B01001_038E,B01001_039E,B01001_040E"
middle = male_middle + "," + female_middle
# Age population 55-74 (elderly): [male]: 
male_elderly = "B01001_017E,B01001_018E,B01001_019E,B01001_020E,B01001_021E,B01001_022E"
# [female]: 
female_elderly = "B01001_041E,B01001_042E,B01001_043E,B01001_044E,B01001_045E,B01001_046E"
elderly = male_elderly + "," + female_elderly

api_pattern = "https://api.census.gov/data/2019/acs/acs1?get=NAME"

url = api_pattern + "," + income + "," + poplation + "," + edu_level + "," + teen + "," + young + "," + middle + "," + elderly + "&for=state:*"

def get_acs_raw():
    """Fetches the raw data of the api link, return dataframe by using pandas"""
    # make request to the url page
    response = requests.get(url)
    
    # check if the request is successful as described in instructions
    if response.status_code == 200:
        # when the request is good to go
        # grab and store the response text, then return the string
        data = response.json()
    
    # refering https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
    # by using pandad convert to a df
    # from row2 to the rest is the content
    # the frist row is header
    df = pd.DataFrame(data[1:], columns=data[0])
    df.to_csv("../data/raw/acs_raw.csv", index=False)

get_acs_raw()

