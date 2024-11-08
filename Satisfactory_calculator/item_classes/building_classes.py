### Here are the attributes for the machines defined

# TODO: Overclocker modifiers to be added here

from common.constants import *

import pandas as pd

class buildings:
    def __init__(self,name:str,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.data_frame = data_frame
        self.attributes = self.find_building()
    
    def find_building(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        sheet_name = next(sheet for sheet in self.data_frame if self.name in self.data_frame[sheet][DC_ITEM].values)
        building_df = self.data_frame[sheet_name]
        building_row = item_df[(item_df[DC_ITEM] == self.name) & (item_df[DC_ITEM_TYPE] == self.item_type)]