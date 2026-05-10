import pandas as pd
# import functions that defined earlier
from clean_data import *

########## Part 1: Merge Dataframe ##########
def merge_df():
    """
    This function will merge all the data that cleaned earlier
    merging them based on same key - "State"
    """
    # call cleaning df function that store cleaned df in a variable
    state_name = clean_state_name()
    gas_price = clean_gas_price()
    ev_reg = clean_ev_reg()
    ev_port = clean_ev_port()
    acs = clean_acs()

    # merging all the df one by one using same key - "State"
    # since state_name df have include extra location
    # using gas price state merging key will avoid NaN rows occur
    df1 = pd.merge(state_name, gas_price, how="right", on="State")
    df2 = pd.merge(df1, ev_reg, how="left", on="State")
    df3 = pd.merge(df2, ev_port, how="left", on="State")
    final_df = pd.merge(df3, acs, how="left", on="State")
    return final_df

########## Part 2: Save Final Dataframe ##########
def save_merged_df(function_name:function, filename:str):
    """
    This function will save the merged df into specific file path
    """
    # save the df that called by input function
    df = function_name
    # set file path
    file_path = "../data/processed/" + filename + ".csv"
    # store the df into a csv file
    df.to_csv(file_path, index=False)

########## Part 3: Function calling ##########
# save the final data into specific file path
save_merged_df(merge_df(), "FINAL_DATA")