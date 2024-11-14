### Here are the attributes of the raw materials in the game defined

# TODO: Node modifiers to be added here

from common.constants import *

from calculations.calculations import item_per_minute

import pandas as pd

class RawMaterial:
    def __init__(self,name:str,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.data_frame = data_frame[DS_RAW]
        self.data_frame = data_frame
        self.attributes = self._find_raw()
    
    def _find_raw(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        raw_row = self.raw_df[(self.raw_df[DC_ITEM] == self.name)]

        if not raw_row.empty:
            attributes = {
                "name": raw_row.iloc[0].get(DC_ITEM, None),
                "output_qty": raw_row.get(DC_ITEM_QTY, 0),
                "output_unit": raw_row.get(DC_ITEM_QTY_UNIT, None),
                "craft_time": raw_row.get(DC_CRAFT_TIME, 1),
                "craft_time_unit": raw_row.get(DC_CRAFT_TIME_UNIT, None),
                "production_facility": raw_row.get(DC_CRAFTED_IN, None),
                "node": raw_row.get(DC_RAW_NODE, None)
            }
            return attributes
        else:
            raise ValueError("Item not found in the data frame")
    
    def get_output_item_per_min(self) -> float:
        '''
        This function calculates the output items per minute.
        '''
        # Initializing a default return
        if "output_qty" not in self.attributes or "craft_time" not in self.attributes:
            return None
        return item_per_minute(self.attributes.get("output_qty"), self.attributes.get("craft_time"))

    def get_production_facility(self)->str:
        '''
        This function returns the crafting facility of the item
        '''
        return self.attributes.get("production_facility", None)