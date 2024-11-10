### This file contains functions that assis working with the data frame of the excel input file


# Importing packages
import pandas as pd
from typing import Optional

# Importing Constants
from common.constants import *


def get_item_row(data_frame:pd.DataFrame, name_col:str, name_filter:str, type_col:str, type_filter:str, sheet:str) -> Optional[pd.Series]:
    ''' 
    Helper to locate the item row based on name and type in a specifc sheet 
    '''
    item_df = data_frame[sheet]
    item_row = item_df[(item_df[name_col] == name_filter) & (item_df[type_col] == type_filter)]

    return item_row.iloc[0] if not item_row.empty else None



