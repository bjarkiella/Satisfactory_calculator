### Here are the attributes for the machines defined

# TODO: Overclocker modifiers to be added here

from common.constants import *
from common.common_checks import check_overclock
from calculations.calculations import overclock_factor
from calculations.calculations import overclock_power

import pandas as pd

class Buildings:
    def __init__(self,name:str,overclock:float,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.data_frame = data_frame[DS_BUILD]
        self.overclock = check_overclock(overclock)
        self.attributes = self._find_building()

    def _find_building(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        building_row = self.data_frame[(self.data_frame[DC_ITEM] == self.name)]

        if not building_row.empty:
            attributes = {
                "name": building_row.iloc[0].get(DC_ITEM, None),
                "power_use": building_row.iloc[0].get(DC_POWER_USE, 0)*overclock_power(self.overclock),
                "power_unit": building_row.iloc[0].get(DC_POWER_UNIT, None),
            }
            return attributes
        else:
            raise ValueError("Item not found in the data frame")

    def get_power_use(self)->float:
        '''
        This function returns the power use of the building
        '''
        return self.attributes.get("power_use", None)
    
    def get_power_unit(self)->str:
        '''
        This function returns the power unit
        '''
        return self.attributes.get("power_unit",None)
