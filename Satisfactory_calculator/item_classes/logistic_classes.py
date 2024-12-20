### Here are the attributes of logistic belts defined
from common.constants import *

from common.error_logs import ErrorLogger

import pandas as pd

class Logistics:     
    def __init__(self, data_frame:pd.DataFrame, required_capacity:float, logger:ErrorLogger) -> None:
        self.data_frame = data_frame[DS_LOG]
        self.required_capacity = required_capacity
        self.logger = logger

    @property
    def attributes(self) -> dict:
        '''
        Internal function that searches for the logistics belt that meets or exceeds the required capacity.
        '''
        # Sort logistics belts by capacity in ascending order to find the smallest sufficient belt
        sorted_belts = self.data_frame.sort_values(by=DC_CAPACITY)

        max_belts = 5
        num_belts = 1
        while num_belts <= max_belts:
            adjusted_capacity = self.required_capacity * num_belts

            for _, row in sorted_belts.iterrows():
                if row[DC_CAPACITY] >= adjusted_capacity:
                    # Return the belt attributes as a dictionary
                    return {
                        "name": row[DC_ITEM],
                        "num_belts": num_belts,
                        "capacity": row[DC_CAPACITY],
                        "capacity_unit": row[DC_CAPACITY_UNIT]
                    }            
            num_belts += 1
        
        # If no belt meets the capacity, raise an exception or handle accordingly
        error_message = "No suitable belt found for the required capacity"
        if self.logger:
            self.logger.log_error(error_message)
        raise ValueError(error_message)
    
    @property
    def log_name(self)->str:
        '''
        This function returns the name of logistic belt
        '''
        return self.attributes.get("name",None)

    @property
    def no_belts(self)->str:
        '''
        This function returns the number of belts required
        '''
        return self.attributes.get("num_belts",None)

    @property
    def log_capacity(self)->float:
        '''
        This function returns the capacity of the logistic item
        '''
        return self.attributes.get("capacity", None)
    
    @property
    def log_unit(self)->str:
        '''
        This function returns the capcity unit
        '''
        return self.attributes.get("capacity_unit",None)

