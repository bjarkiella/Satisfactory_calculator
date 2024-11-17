### Here are the attributes for the machines defined

from common.constants import *
from common.common_checks import check_overclock
from calculations.calculations import overclock_factor
from calculations.calculations import overclock_power

from common.error_logs import ErrorLogger

import pandas as pd

class Buildings:
    def __init__(self,name:str,overclock:float,data_frame:pd.DataFrame,logger:ErrorLogger) -> None:
        self.name = name
        self.data_frame = data_frame[DS_BUILD]
        self.overclock = check_overclock(overclock)
        self.logger = logger

    @property
    def attributes(self) -> dict:
        '''
        Dynamically and finds and returns the building attributes
        '''
        building_row = self.data_frame[(self.data_frame[DC_ITEM] == self.name)]
        
        if not building_row.empty:
            return {
                "name": building_row.iloc[0].get(DC_ITEM, None),
                "power_use": building_row.iloc[0].get(DC_POWER_USE, 0)*overclock_power(self.overclock),
                "power_unit": building_row.iloc[0].get(DC_POWER_UNIT, None),
            }
        else:
            error_message = f"Building '{self.name}' not found in the data frame."
            if self.logger:
                self.logger.log_error(error_message)
            raise ValueError(error_message)

    @property
    def power_use(self) -> float:
        '''
        Returns the power use of the building dynamically.
        '''
        return self.attributes.get("power_use", 0)

    @property
    def power_unit(self) -> str:
        '''
        Returns the power unit of the building dynamically.
        '''
        return self.attributes.get("power_unit", None)
