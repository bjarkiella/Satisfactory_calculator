### This file contains functions that assis working with the data frame of the excel input file

# Importing packages
from pandas import DataFrame

# Importing Constants
from common.constants import DATA_COLUMN_ITEM

def find_item(dfs:DataFrame, requested_item:str) -> dict:
    '''
    This function finds an item name 
    '''
    req_item_dict = {}
    for sheet_name, df in dfs.items():
        if DATA_COLUMN_ITEM in df.columns:  # Checking if the item column is available in the sheet
            item_row = df[df[DATA_COLUMN_ITEM] == requested_item]

            if not item_row.empty:
                req_item_dict = item_row.iloc[0].to_dict()  # Get the first row and convert to dictionary
                break

    return req_item_dict

