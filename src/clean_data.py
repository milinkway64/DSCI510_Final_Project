import pandas as pd

########## Part 1: Clean Raw Data: txt format ##########
def clean_state_name():
    """
    This function is used to clean the state name and its abbr
    convert txt to csv file
    """
    # data file path
    file = "../data/raw/state_name_raw.txt"
    # open the raw data file in reading mode
    with open(file, "r") as file:
        # create a list to store state full name
        name_lst = []
        # create a list to store state's corresponding abbr
        abbr_lst = []
        # read each line in file instead of a whole string
        lines = file.readlines()
        # as every 2 line is for one state, loop through every 2 steps
        for i in range(0, len(lines), 2):
            # even lines is state full name(python counts from 0)
            # using strip to remove empty space or \n
            state = lines[i].strip()
            # append the name_lst with full state name
            name_lst.append(state)
            # repeat same process for state abbr
            # odd lines is state abbr
            abbr = lines[i+1].strip()
            abbr_lst.append(abbr)

        # create a dict for later df converting use
        state_dict = {}
        # update the dict with df column name
        state_dict["State"] = name_lst
        state_dict["Abbr"] = abbr_lst
        # convert dict to df
        df = pd.DataFrame(state_dict)
        return df

def clean_gas_price():
    """
    This function is used to clean the gas price in each state
    and give a ranking col of gas price in each state
    convert txt to csv file
    """
    # raw data file path
    file = "../data/raw/gas_price_raw.txt"
    # open the data file in reading mode
    with open(file, "r") as file:
        # create a list to store state name
        state_lst = []
        # create a list to store gas price in each state
        price_lst = []
        # reading the file as lines
        lines = file.readlines()
        # as every 3 line is for one state info, loop through every 3 steps
        for i in range(0, len(lines), 3):
            # since the first item for each state is non-important info
            # the data collection from second element
            # state is the second element
            # remove empty space or change lines then append the list
            state = lines[i+1].strip()
            state_lst.append(state)
            # repeat the same process for gas price
            # gas price is 3rd element
            price = lines[i+2].strip()
            # since the dollar symbol was includes and that will be a string
            # clear the dollar symbol for later statistical use
            price = price.replace("$", "")
            price_lst.append(price)
        
        # create a dict for later df converting use
        price_dict = {}
        # update the dict with later column name
        price_dict["State"] = state_lst
        price_dict["gas_price"] = price_lst
        # convert to df
        df = pd.DataFrame(price_dict)
        # exclude rows that is not for states
        df = df[df["State"] != "United States"]
        # clean the gas price data, as some typo may exist
        df["gas_price"] = df["gas_price"].str.replace(",", ".")
        # make sure the gas price is float not string
        df = df.astype({"gas_price": float})
        # add a column that containing gas price ranking for each state
        # use method="min" to handle tie
        # use ascending=False as the ranking 1 is the highest price
        df["gas_price_rank"] = df["gas_price"].rank(method="min", ascending=False)
        # ranking should be int
        df = df.astype({"gas_price_rank": int})
        return df
    
########## Part 2: Clean Raw Data: csv format ##########
def clean_ev_reg():
    """
    This function is used to clean the car registration csv
    in this function, it will calculate the EV adoptation rate
    and the rate ranking for each state
    """
    # raw data file path
    file = "../data/raw/ev_reg_raw.csv"
    # read the csv into df
    df = pd.read_csv(file)
    # calculte a total registration counts that for all types cars
    df["Total"] = df.sum(axis=1, numeric_only=True)
    # calculate the EV registration rate in percentage
    df["EV_rate"] = df["Electric (EV)"] / df["Total"] * 100
    # grab the columns will need
    # instead of massive dropping
    df1 = df[["State", "EV_rate"]]
    # round the EV rate percentage for clearness
    df1 = df1.round(3)
    # exclude rows that is not state
    df1 = df1[df1["State"] != "United States"]
    # add a column that containing ev rate ranking for each state 
    # use method="min" to handle tie
    # use ascending=False as the ranking 1 is the highest adoptation rate
    df1["EV_rate_rank"] = df1["EV_rate"].rank(method="min", ascending=False)
    # ranking should be int
    df1 = df1.astype({"EV_rate_rank": int})
    return df1

def clean_ev_port():
    """
    This function is used to clean the ev charging ports stations csv
    In this function will rebuild the columns from the raw data
    create a station counts ranking
    """
    # raw data file path
    file = "../data/raw/ev_port_raw.csv"
    # open the data in df
    df = pd.read_csv(file)
    # give each columns name, as raw data was empty and chaos
    df.columns = [
    "State", "Biodiesel", "CNG", "E85",
    "Electric", "Hydrogen", "LNG",
    "Propane", "Renewable_Diesel", "Total"]
    # as the format of raw data was chaos
    # each 2 lines is a state info
    # create a empty dataframe to seperate the rows
    first_row_df = pd.DataFrame()
    # since each 2 rows is for one state and we only need the first row
    # looping over steps is 2
    for i in range(0, len(df), 2):
        # the row that will add to the first_row_df
        # iloc is use to find which row
        new_row = df.iloc[[i]]
        # expand the first_row_df by adding the rows
        first_row_df = pd.concat([first_row_df, new_row], ignore_index=True)
    # create the final df that grabing the cols needed from cleared first_row_df
    final_df = first_row_df[["State", "Electric"]]
    # split the column by using string split
    # ex.: "stations|outlets" --> "stations" "outlets"
    # using n=1 to limit the split process
    # expand=True that makes the splited string into cols not list
    final_df[["Stations", "Outlets"]] = final_df["Electric"].str.split('|', n=1, expand=True)
    # after split, drop the columns that not need
    final_df = final_df.drop(columns=["Electric", "Outlets"])
    # exclude the rows that the state is not a state
    final_df = final_df[final_df["State"] != "Total"]
    # clear the data from a string to number
    final_df["Stations"] = final_df["Stations"].str.replace(",", "")
    final_df = final_df.astype({"Stations": int})
    # add a column that ranks the count of stations
    final_df["Station_rank"] = final_df["Stations"].rank(method="min", ascending=False)
    final_df = final_df.astype({"Station_rank": int})
    return final_df

def clean_acs():
    """
    In this function, all variable name will convert from code to real meaning
    and will calculate a seris of population percentage based on age range 
    and high education level, after cleaning and calculation,
    income ranking will be added
    """
    # get the data
    file = "../data/raw/acs_raw.csv"
    df = pd.read_csv(file)

    # rename partial columns for easier access
    column_name = {
        "NAME" : "State",
        "B19013_001E" : "Median_Income",
        "B01003_001E" : "Population"
    }
    df = df.rename(columns=column_name)
    
    # before calculating convert string to number
    # as I checked dtypes
    for columns in df.columns:
        # exclude the state names
        # else convert to number
        if columns not in ["State", "state"]:
            df[columns] = pd.to_numeric(df[columns])

    # calculate higher educated level
    # using column: B15003_001E(total),B15003_022E(bach),B15003_023E(master)
    # B15003_024E(prof),B15003_025E(doc)
    df["High_Edu_Level_Percent"] = ((df["B15003_022E"] + df["B15003_023E"] + 
                                     df["B15003_024E"] + df["B15003_025E"]) / 
                                     (df["B15003_001E"])) * 100
    # after calculation, drop unnecessary columns
    df = df.drop(columns=["B15003_022E", "B15003_023E", "state",
                          "B15003_024E", "B15003_025E", "B15003_001E"])
    
    # calculate the teen pop percentage (15-24)
    # using B01001_006E,B01001_007E,B01001_008E,B01001_009E,B01001_010E
    # B01001_030E,B01001_031E,B01001_032E,B01001_033E,B01001_034E
    df["Teen_Population"] = (df["B01001_006E"] + df["B01001_007E"] + df["B01001_008E"] + 
                             df["B01001_009E"] + df["B01001_010E"] + df["B01001_030E"] + 
                             df["B01001_031E"] + df["B01001_032E"] + df["B01001_033E"] + 
                             df["B01001_034E"])
    df["Teen_Percent"] = (df["Teen_Population"] / df["Population"]) * 100
    # after calculation, drop unnecessary columns
    df = df.drop(columns=["B01001_006E", "B01001_007E",
                          "B01001_008E", "B01001_009E", "B01001_010E",
                          "B01001_030E", "B01001_031E",
                          "B01001_032E", "B01001_033E", "B01001_034E", "Teen_Population"])
    
    # calculate the young pop percentage (25-34)
    # using B01001_011E,B01001_012E,B01001_035E,B01001_036E
    df["Young_Percent"] = (((df["B01001_011E"] + df["B01001_012E"] +
                             df["B01001_035E"] + df["B01001_036E"]) 
                            / df["Population"]) * 100)
    # after calculation, drop unnecessary columns
    df = df.drop(columns=["B01001_011E", "B01001_012E",
                          "B01001_035E", "B01001_036E"])
    
    # calculate the middle pop percentage (35-54)
    # using "B01001_013E,B01001_014E,B01001_015E,B01001_016E,B01001_037E,B01001_038E,B01001_039E,B01001_040E"
    df["Middle_Population"] = (df["B01001_013E"] + df["B01001_014E"] + df["B01001_015E"] + 
                             df["B01001_016E"] + df["B01001_037E"] + df["B01001_038E"] + 
                             df["B01001_039E"] + df["B01001_040E"])
    df["Middle_Percent"] = (df["Middle_Population"] / df["Population"]) * 100
    # after calculation, drop unnecessary columns
    df = df.drop(columns=["B01001_013E", "B01001_014E","B01001_015E",
                          "B01001_016E","B01001_037E", "B01001_038E",
                          "B01001_039E", "B01001_040E", "Middle_Population"])
    
    # calculate the elderly pop percentage (55-74)
    # using ""B01001_017E,B01001_018E,B01001_019E,B01001_020E,B01001_021E,B01001_022E,
    # B01001_041E,B01001_042E,B01001_043E,B01001_044E,B01001_045E,B01001_046E"
    df["Elderly_Population"] = (df["B01001_017E"] + df["B01001_018E"] + df["B01001_019E"] + 
                             df["B01001_020E"] + df["B01001_021E"] + df["B01001_022E"] + 
                             df["B01001_041E"] + df["B01001_042E"] + df["B01001_043E"] + 
                             df["B01001_044E"] + df["B01001_045E"]  + df["B01001_046E"])
    df["Elderly_Percent"] = (df["Elderly_Population"] / df["Population"]) * 100
    # after calculation, drop unnecessary columns
    df = df.drop(columns=["B01001_017E", "B01001_018E","B01001_019E",
                          "B01001_020E","B01001_021E", "B01001_022E",
                          "B01001_041E", "B01001_042E", "B01001_043E",
                          "B01001_044E", "B01001_045E", "B01001_046E",
                          "Elderly_Population", "Population"])
    # add a col that ranks income
    df["Income_rank"] = df["Median_Income"].rank(method="min", ascending=False)
    df = df.astype({"Income_rank": int})
    # rounding all numbers/rates into 3 decimal places
    df = df.round(3)
    return df

########## Part 3: Save Cleaned Data in csv ##########
def save_cleaned_df(function_name:function, filename:str):
    """
    This function will save the cleaned dataframe into a csv file
    on specific file path that defined in input filename
    """
    df = function_name
    file_path = "../data/processed/" + filename + ".csv"
    df.to_csv(file_path, index=False)

########## Part 4: Function Calling ##########
# the follwing functions was called to save the cleared dataframe
save_cleaned_df(clean_state_name(), "state_abbr")
save_cleaned_df(clean_gas_price(), "gas_price")
save_cleaned_df(clean_ev_reg(), "ev_reg")
save_cleaned_df(clean_ev_port(), "ev_port")
save_cleaned_df(clean_acs(), "acs")