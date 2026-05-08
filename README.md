# DSCI510_Final_Project
Author: Minyun Wang

### Project Description:

### Repository Structure/File Routine
In this repository, there are 3 major folders and several supportive files.

---
# `get_data.py`
In this coding file, all the functions are designed to pull raw data from web and store in the `data/raw` folder.

There are 4 parts in this coding file, will explaned one by one and a **How to work** section:
- Part 1: Web Table Data Scraper
- Part 2: Using Pandas to Extract data
- Part 3: 2023 ACS Extraction
- Part 4: Calling Functions to Get Raw Data

## Part 1: Web Table Data Scraper
`web_scrape(url:str, file_name:str, table_nums:int)`:

This function is used to store a `.txt` file containing all tables extracted from a web page. Since both the `state and abbreviation` data and the `2023 gasoline price by state` data use the same scraping method, this function is designed to use for both data web pages.

Input Explanation:
- `url`: This is a string input which indicate the url link.
- `file_name`: This is a string input used for file name path set up.
- `table_nums`: This is a int input used for extract how many tables is wanted from the url page. 

## Part 2: Using Pandas to Extract data
`pds_extract(url:str, file_name:str)`:

This function is used to store a `.csv` raw data file which containg tables extracted from *afdc.energy.gov*. Since the `EV registration in 2023` and `EV charging ports in 2023` data use the same extracting method by pandas, this function is designed to use for both datasets. 

Input Explanation:
- `url`: This is a string input which indicate the url link.
- `file_name`: This is a string input used for file name path set up.

## Part 3: 2023 ACS Extraction
In this part there the first part is pre-set for url link and second part is the function to extract data then save as a `.csv` file.

All the variable name could refer to https://api.census.gov/data/2023/acs/acs1/variables.html. For api capture info could refer to https://www.census.gov/data/developers/data-sets/acs-1year.2023.html#list-tab-843855098.

Variable Name Index：
- `B19013_001E`: income
- `B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E`: education level population
- `B01001_006E,B01001_007E,B01001_008E,B01001_009E,B01001_010E`: male(15-24) population
- `B01001_030E,B01001_031E,B01001_032E,B01001_033E,B01001_034E`: female(15-24) population
- `B01001_011E,B01001_012E`: male(25-34) population
- `B01001_035E,B01001_036E`: female(25-34) population
- `B01001_013E,B01001_014E,B01001_015E,B01001_016E`: male(35-54) population
- `B01001_037E,B01001_038E,B01001_039E,B01001_040E`: female(35-54) population
- `B01001_017E,B01001_018E,B01001_019E,B01001_020E,B01001_021E,B01001_022E`: male(55-74) population
- `B01001_041E,B01001_042E,B01001_043E,B01001_044E,B01001_045E,B01001_046E`: female(55-74) population

By merging variable name and api capture info, the url is created and stored in `url` variable.

`get_acs_raw()`
This function is used to store a `.csv` file that stores the ACS 2023 data, which can be directly called. 

## Part 4: Calling Functions to Get Raw Data
In this part, all data link was store to its correspond variable and then call all the functions defined earlier, then the raw data file will be stored as file path that defined in the functions. 

Data Links:
- State name and its abbr: `https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html`
- Gasoline price in 2023: `https://www.visualcapitalist.com/mapped-gas-prices-in-every-u-s-state/` 
- EV car registration in 2023: `https://afdc.energy.gov/vehicle-registration?year=2023` 
- EV ports counts in 2023: `"https://afdc.energy.gov/stations/states?count=total&include_temporarily_unavailable=false&date=2023-12-31"`
- ***p.s.*** ACS 2023 dataset link was defined in the coding file

## How do `get_data.py` work
Run following code in terminal:
```python
python3 get_data.py
```
All Raw data files will stored in `data/raw` folder accordingly.

---

# `clean_data.py`