### Here are the attributes for the machines defined

# TODO: Overclocker modifiers to be added here

from common.constants import *

import pandas as pd

class Buildings:
    def __init__(self,name:str,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.data_frame = data_frame
        self.attributes = self._find_building()
    
    def _find_building(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        building_df = self.data_frame[DS_BUILD]
        building_row = building_df[(building_df[DC_ITEM] == self.name)]

        if not building_row.empty:
            attributes = {
                "name": building_row.iloc[0].get(DC_ITEM, None),
                "power_use": building_row.iloc[0].get(DC_POWER_USE, 0),
                "power_unit": building_row.iloc[0].get(DC_POWER_UNIT, None)
            }
            return attributes
        else:
            raise ValueError("Item not found in the data frame")

    def get_power_use(self)->float:
        '''
        This function returns the power use of the building
        '''
        return self.attributes.get("power_use", None)