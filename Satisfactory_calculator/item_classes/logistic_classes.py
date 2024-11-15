### Here are the attributes of logistic belts defined
from common.constants import *

import pandas as pd

class Logistics:
    # def __init__(self,name:str,data_frame:pd.DataFrame) -> None:
    #     self.name = name
    #     self.data_frame = data_frame
    #     self.attributes = self._find_logistics()
    #     self.data_frame = data_frame(DS_LOG)
     
    def __init__(self, data_frame:pd.DataFrame, required_capacity:float) -> None:
        self.data_frame = data_frame[DS_LOG]
        self.required_capacity = required_capacity
        self.attributes = self._find_logistics()
      
        

    def _find_logistics(self) -> dict:
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
                    attributes ={
                        "name": row[DC_ITEM],
                        "num_belts": num_belts,
                        "capacity": row[DC_CAPACITY],
                        "capacity_unit": row[DC_CAPACITY_UNIT]
                    }
                    return attributes
            
            num_belts += 1
        
        # If no belt meets the capacity, raise an exception or handle accordingly
        raise ValueError("No suitable belt found for the required capacity")

    # def _find_logistics(self) -> dict:
    #     '''
    #     This function searches the data frame for the requested item and type and gives it the attributes
    #     '''
    #     logistics_df = self.data_frame[DS_LOG]
    #     logistics_row = logistics_df[(logistics_df[DC_ITEM] == self.name)]

    #     if not logistics_row.empty:
    #         attributes = {
    #             "name": logistics_row.iloc[0].get(DC_ITEM, None),
    #             "capacity": logistics_row.iloc[0].get(DC_CAPACITY, 0),
    #             "capacity_unit": logistics_row.iloc[0].get(DC_CAPACITY_UNIT, None)
    #         }
    #         return attributes
    #     else:
    #         raise ValueError("Item not found in the data frame")


    def get_log_name(self)->str:
        '''
        This function returns the name of logistic belt
        '''
        return self.attributes.get("name",None)

    def get_no_belts(self)->str:
        '''
        This function returns the number of belts required
        '''
        return self.attributes.get("num_belts",None)

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

    # def find_belt_for_capacity(self, required_capacity:float)->dict:
    #     '''
    #     This function returns the item row
    #     '''
    #     return self.attributes