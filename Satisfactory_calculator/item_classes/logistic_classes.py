### Here are the attributes of logistic belts defined
from common.constants import *

import pandas as pd

class Logistics:
    def __init__(self,name:str,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.data_frame = data_frame
        self.attributes = self._find_logistics()
    
    def _find_logistics(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        logistics_df = self.data_frame[DS_LOG]
        logistics_row = logistics_df[(logistics_df[DC_ITEM] == self.name)]

        if not logistics_row.empty:
            attributes = {
                "name": logistics_row.iloc[0].get(DC_ITEM, None),
                "capacity": logistics_row.iloc[0].get(DC_CAPACITY, 0),
                "capacity_unit": logistics_row.iloc[0].get(DC_CAPACITY_UNIT, None)
            }
            return attributes
        else:
            raise ValueError("Item not found in the data frame")


    def get_log_capacity(self)->float:
        '''
        This function returns the capacity of the logistic item
        '''
        return self.attributes.get("capacity", None)
    
    def get_log_unit(self)->str:
        '''
        This function returns the capcity unit
        '''
        return self.attributes.get("capacity_unit",None)