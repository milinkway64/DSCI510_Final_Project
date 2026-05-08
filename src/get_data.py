import requests
from bs4 import BeautifulSoup
import pandas as pd

########## Part 1: Web Table Data Scraper ##########
def web_scrape(url:str, file_name:str, table_nums:int):
    """
    This function will scrape the raw table data from the input url. 
    Designed for scraping (state name and abbr) and (2023 gasoline price) table from 2 websites
    The raw data will be stored in ../data/raw folder.
    url is the link of the web with the table
    file_name is used for set up the file path 
    table_nums is used to locate how many tables is needed
    """
    # make request to the input url page
    response = requests.get(url)
    # check if the request is successful
    if response.status_code == 200:
        # grab and store the response text when the request is successful
        html_content = response.text
    
    # parse the HTML content by using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    # find the table element in the web page
    # using table_nums to define how many tables extracted
    tables = soup.find_all("table")[:table_nums]
    # create a list to store all text data
    lst = []
    # go through all elements
    for table in tables:
        rows = table.find_all("td")
        for item in rows:
            lst.append(item.text.strip())

    # create the raw data file path
    txt = "../data/raw/" + file_name + ".txt"
    # write the file with list content
    with open(txt, "w") as file:
        # go through the list then
        # write each line of state name and abbreviation
        for item in lst:
            file.write(item + "\n")

########## Part 2: Using Pandas to Extract data ##########
def pds_extract(url:str, file_name:str):
    """
    This function will extract data of EV related data from afdc.energy.gov
    Using pandas to get the dataframe
    url is input of the target web link
    file_name is used to set the file path name
    """
    # by using pd.read_html() to extract tables from the web page
    tables = pd.read_html(url)
    # select the target table store in df
    df = tables[0]
    # create the raw data file path
    file_path = "../data/raw/" + file_name + ".csv"
    # save the df into a csv file
    df.to_csv(file_path, index=False)

########## Part 3: 2023 ACS Extraction ##########
# 2023 link pre-setup
# following 'BXXXXX_XXXE'is the name of variable
# refer to census variable page get the related name
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

api_pattern = "https://api.census.gov/data/2023/acs/acs1?get=NAME"

url = api_pattern + "," + income + "," + poplation + "," + edu_level + "," + teen + "," + young + "," + middle + "," + elderly + "&for=state:*"

def get_acs_raw():
    #Fetches the raw data of the api link, return dataframe by using pandas
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

########## Part 4: Calling Functions to Get Raw Data ##########
# State name and its abbr
state_name = "https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html"
web_scrape(state_name, "state_name_raw", 1)

# Gasoline price in 2023
gas_price = "https://www.visualcapitalist.com/mapped-gas-prices-in-every-u-s-state/"
web_scrape(gas_price, "gas_price_raw", 2)

# EV car registration in 2023
ev_reg = "https://afdc.energy.gov/vehicle-registration?year=2023"
pds_extract(ev_reg, "ev_reg_raw")

# EV ports counts in 2023
ev_port = "https://afdc.energy.gov/stations/states?count=total&include_temporarily_unavailable=false&date=2023-12-31"
pds_extract(ev_port, "ev_port_raw")

# 2023 ACS data
get_acs_raw()