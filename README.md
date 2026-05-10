# DSCI510_Final_Project
Author: Minyun Wang

### Project Description:
This project is designed to answer the question: **What factors impact EV adoption?**  

Five datasets are used to analyze the question with a total of eight factors, including `gas price`, `charging station counts`, `income`, `education level`, and four `age group` variables. After cleaning and merging the data, visualizations are generated to examine the relationships between these factors and EV adoption rates.

All Dataset usage and python library guidance will be cited in the report.

### Repository Structure/File Routine
In this repository, there are 3 major folders and several supportive files.

```text
DSCI510_Final_Project/
├── README.md
├── requirements.txt  # all the packages need to install for python coding file
├── proposal.pdf
├── data/
│   ├── raw/          # raw datasets collected from sources in .txt and .csv file type
│   └── processed/    # cleaned datasets all in .csv file type
├── results/
│   ├── final_report.pdf
│   └── plots/        # final plots will be stored here, interactive graph in .html, other in .png
├── src/
│   ├── get_data.py
│   ├── clean_data.py
│   ├── integrate_data.py
│   └── analyze_visualize.py
```

---
# `get_data.py`
In this coding file, all the functions are designed to pull raw data from web and store in the `data/raw` folder. All function use was guided/referenced from package library, please see citiation in `final_report.pdf`. 

There are 4 parts in this coding file, will explaned one by one and a **How to work** section:
- Part 1: Web Table Data Scraper
- Part 2: Using Pandas to Extract data
- Part 3: 2023 ACS Extraction
- Part 4: Function Calling

## Part 1: Web Table Data Scraper
### `web_scrape(url:str, file_name:str, table_nums:int)`:

This function is used to store a `.txt` file containing all tables extracted from a web page. Since both the `state and abbreviation` data and the `2023 gasoline price by state` data use the same scraping method, this function is designed to use for both data web pages.

Input Explanation:
- `url`: This is a string input which indicate the url link.
- `file_name`: This is a string input used for file name path set up.
- `table_nums`: This is a int input used for extract how many tables is wanted from the url page. 

## Part 2: Using Pandas to Extract data
### `ev_reg_raw()`:
This function scrape the data table from the web of ***afdc.energy.gov***. By using `.read_html()` from pandas package to get the `car registration` table then turn into dataframe. Then store the data in a `csv` file in assigned file path. 

### `ev_port_raw()`:
This function is used to scrape the excel data from ***afdc.energy.gov***. By using `.read_excel` to get the data of `ev charging ports numbers` and convert as a dataframe. Then store the raw data in a `csv` file in assigned file path. 

## Part 3: 2023 ACS Extraction
In this part, there 2 sections, first section is pre-set for url link and second section is the function to extract data then save as a `.csv` file.

- For api capture info could refer to https://www.census.gov/data/developers/data-sets/acs-1year.2023.html#list-tab-843855098.

Variable Name Index
- Income (`B19013_001E`)
- Education levels (`B15003_*`)
- Population by age and gender (`B01001_*`)
- For full variable definitions, see: https://api.census.gov/data/2023/acs/acs1/variables.html

By merging variable name and api capture info, the url is created and stored in `url` variable.

#### `get_acs_raw()`
This function is used to store a `.csv` file that stores the ACS 2023 data, which can be directly called. 

## Part 4: Function Calling
In this part, all data link was store to its correspond variable and then call all the functions defined earlier, then the raw data file will be stored as file path that defined in the functions. 

Data Links:
- State name and its abbr: `https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html`
- Gasoline price in 2023: `https://www.visualcapitalist.com/mapped-gas-prices-in-every-u-s-state/` 
- ***p.s.*** Other dataset link was defined in the coding file

## How do `get_data.py` work
Run the following command in the terminal (make sure you are in the project root directory):
```python
python3 src/get_data.py
```
All Raw data files will stored in `data/raw` folder accordingly.

***PS.*** There is a small chance that if a Error raise for `web_scrape(gas_price, "gas_price_raw", 2)` due to changes in the source website, if re-run the file doesn't work, please open the following link:

https://www.visualcapitalist.com/mapped-gas-prices-in-every-u-s-state/

Then update the URL assigned to the `gas_price` variable (line 122 in the script).  
After updating, save the file and rerun the script.

---

# `clean_data.py`
In this python coding file, all functions are designed to clean the raw data file that created by `get_data.py`, after cleaning process the cleared data file will be saved in `data/processed` folder as `csv` files. All function use was guided/referenced from package library, please see citiation in `final_report.pdf`. 

There are 4 parts in this coding file, will explaned one by one and a **How to work** section:
- Part 1: Clean Raw Data: `txt` format
- Part 2: Clean Raw Data: `csv` format
- Part 3: Save Cleaned Data in `csv`
- Part 4: Function Calling

## Part 1: Clean Raw Data: `txt` format
### `clean_state_name()`
This function is used to clean the `state name and abbr` dataset, and finally will return the cleared data as a `dataframe`. The final dataframe will contain `State` and `Abbr` variable for futher use. 

### `clean_gas_price()`
This function is used to clean the `gas price` dataset, and return the cleared data as a `dataframe`. The cleaned data will contain `State`, `gas_price`, and `gas_price_rank` for futher use. 

## Part 2: Clean Raw Data: `csv` format
### `clean_ev_reg()`
This function is used to clean `ev registration` file, and calculate ratio variables for further use. In the function, data will be cleared, calculated, and converted to target variable type. Finally, the function will return a `dataframe`. 

### `clean_ev_port()`
In this function, `ev charging ports` data will be cleared, calculted and converted to target variable type. And the function will return a `dataframe`. 

### `clean_acs()`
This function will clean the `ACS` dataset, by renaming, calculating, and converting value type. After cleaning process the function will return the cleaned data `dataframe`. 

## Part 3: Save Cleaned Data in `csv`
### `save_cleaned_df(function_name:function, filename:str)`
This function will take 2 required inputs, which will save the cleaned dataframe as a `csv` file in `data/processed` folder.

Input Explanation:
- `function_name`: This is a function input which should input the cleaning function that returns a dataframe.
- `filename`: This is a string input used for file name path set up.

## Part 4: Function Calling
In this part, `save_cleaned_df()` was called to store all cleared dataset as `csv` file into `data/processed` folder.

## How do `clean_data.py` work
Run the following command in the terminal (make sure you are in the project root directory):
```python
python3 src/clean_data.py
```
All cleaned data files will stored in `data/processed` folder accordingly.

---
# `intergrate_data.py`
This python coding file is used to merge all cleaned data into one dataframe then saved as a final data `csv` file into `data/processed`. Also import all the functions from the `clean_data.py` can directly get the cleaned dataframes.

There are 3 parts in this coding file, will explaned one by one and a **How to work** section:
- Part 1: Merge Dataframe
- Part 2: Save Final Dataframe
- Part 3: Function Calling

## Part 1: Merge Dataframe
### `merge_df()`
This function will merge all the datasets into one dataframe based on one primary key `"State"`, after all merging process, will return the final data as a dataframe.

## Part 2: Save Final Dataframe
### `save_merged_df(function_name:function, filename:str)`
This function will take 2 required inputs, which will save the final dataframe as a `csv` file in `data/processed` folder.

Input Explanation:
- `function_name`: This is a function input which should input the cleaning function that returns a dataframe.
- `filename`: This is a string input used for file name path set up.

## Part 3: Function Calling
In this part, `save_merged_df()` was called to store Final merged dataset as `FINAL_DATA.csv` file into `data/processed` folder.

## How do `integrate_data.py` work
Run the following command in the terminal (make sure you are in the project root directory):
```python
python3 src/integrate_data.py
```
The final data files will stored in `data/processed` folder as `FINAL_DATA.csv` accordingly.

---
# `analyze_visualize.py`
In this coding file, functions are designed to plot visualizations to support analyze. All function use was guided/referenced from package library, please see citiation in `final_report.pdf`. After runing the code file, all plots will be saved into `results/plots` folder. 

There are 5 parts in this coding file, will explaned one by one and a **How to work** section:
- Part 1: General Info Graph
- Part 2: Linear Regression graphs
- Part 3: Distribution Graph
- Part 4: Statistical Results Table
- Part 5: Function Calling

## Part 1: General Info Graph
### `plot_EV_rate_info()`
This function will plot an interactive choropleth map by using `plotly.express.choropleth()`. This plot is designed to see and comparing `ev_adoption_rate` by color, the lighter the blue, the lower the adoption rate. Also, when hover over each state can see some additional information which includes some factor's ranking. 

The interactive graphs are saved in both `.png` and `.html` formats.
- The `.png` file provides a preview that can be viewed directly on GitHub.  
- The `.html` file contains the full interactive version of the graph. Since GitHub does not show `.html` files, please download the file and open it locally to view the interactive features.

## Part 2: Linear Regression graphs
### `plot_non_age_factor()`
This function will generate a figure with 4 subplots by using `matplotlib.pyplot` and `sns.regplot()`, that each showing a linear regression plot of one non-age factor and ev adoption rate. 

### `plot_age_factor()`
This function will generate a figure with 4 subplots by using `matplotlib.pyplot` and `sns.regplot()`, that each showing a linear regression plot of one age-related factor and ev adoption rate. 

## Part 3: Distribution Graph
This function will produce a distribution plot of ev adpotation rate with some customized design, by using `matplotlib.pyplot`.

## Part 4: Statistical Results Table
### `stats_table_df()`
This function creates the dataframe of `r-value` and `p-value` of each factors. The statistical calcultaion was calculated by `scipy`packages. 

### `plot_stats_table()`
By using the `plotly.graph_objects`, this function creates a table plot that shows each factor's `r-value` and `p-value`.

## Part 5: Function Calling
In this part, all `plot_` series functions will be called to store all plots image into `results/plots` folder, either as a `png` file or `html` file.

## How do `analyze_visualize.py` work
Run the following command in the terminal (make sure you are in the project root directory):
```python
python3 src/analyze_visualize.py
```
All visual plots will stored in `results/plots` folder as `png` and an interactive plot saved in `html` accordingly.