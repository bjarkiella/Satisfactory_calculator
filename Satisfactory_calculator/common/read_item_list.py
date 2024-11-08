### This file contains functions that assis working with the data frame of the excel input file
### This might be an obsolete file


# Importing packages
from pandas import DataFrame

# Importing Constants
from common.constants import DC_ITEM
from common.constants import DC_ITEM_TYPE

def find_item(dfs:DataFrame, requested_item:str, requested_item_type:str = None) -> dict:
    '''
    This function finds the item and its type in the dfs data frame
    '''
    req_item_dict = {}
    for sheet_name, df in dfs.items():
        if DC_ITEM in df.columns:  # Checking if the item column is available in the sheet
            if DC_ITEM_TYPE in df.columns: # Checking if the item type column is available in the sheet
                item_row = df[(df[DC_ITEM] == requested_item) & (df[DC_ITEM_TYPE] == requested_item_type)]
            else:
                item_row = df[(df[DC_ITEM] == requested_item)]
            if not item_row.empty:
                # if df[dc_item_type] == requested_item_type: # checking if the item types match
                    # req_item_dict[sheet_name] = {}
                req_item_dict[sheet_name] = item_row.iloc[0].to_dict()  # Get the first row and convert to dictionary
                break

    return req_item_dict

