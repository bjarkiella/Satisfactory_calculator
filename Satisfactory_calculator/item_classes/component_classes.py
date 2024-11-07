### Here are the attributes of the items setup in a class


from common.constants import *
import pandas as pd


class Item:
    def __init__(self,name:str,item_type:str,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.item_type = item_type
        self.data_frame = data_frame
        self.attributes = self.find_item()
    
    def find_item(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        sheet_name = next(sheet for sheet in self.data_frame if self.name in self.data_frame[sheet][DC_ITEM].values)
        item_df = self.data_frame[sheet_name]
        item_row = item_df[(item_df[DC_ITEM] == self.name) & (item_df[DC_ITEM_TYPE] == self.item_type)]


        if not item_row.empty:
            attributes = {
                "name":item_row.iloc[0][DC_ITEM],
                "output_qty": item_row.iloc[0][DC_ITEM_QTY],
                "output_unit": item_row.iloc[0][DC_ITEM_QTY_UNIT],
                "extra_item": item_row.iloc[0][DC_EXTRA_ITEM],
                "extra_item_qty": item_row.iloc[0][DC_EXTA_ITEM_QTY],
                "extra_item_unit": item_row.iloc[0][DC_EXTA_ITEM_UNIT],
                "craft_time": item_row.iloc[0][DC_CRAFT_TIME],
                "craft_time_unit": item_row.iloc[0][DC_CRAFT_TIME_UNIT],
                "input_materials": [
                    {
                        "material": item_row.iloc[0][DC_INPUT_MAT_1],
                        "quantity": item_row.iloc[0][DC_INPUT_QTY_1],
                        "unit": item_row.iloc[0][DC_INPUT_QTY_UNIT_1]
                    },
                    {
                        "material": item_row.iloc[0][DC_INPUT_MAT_2],
                        "quantity": item_row.iloc[0][DC_INPUT_QTY_2],
                        "unit": item_row.iloc[0][DC_INPUT_QTY_UNIT_2]
                    },
                    {
                        "material": item_row.iloc[0][DC_INPUT_MAT_3],
                        "quantity": item_row.iloc[0][DC_INPUT_QTY_3],
                        "unit": item_row.iloc[0][DC_INPUT_QTY_UNIT_3]
                    },
                    {
                        "material": item_row.iloc[0][DC_INPUT_MAT_4],
                        "quantity": item_row.iloc[0][DC_INPUT_QTY_4],
                        "unit": item_row.iloc[0][DC_INPUT_QTY_UNIT_4]
                    }
                ],
                "production_facility": item_row.iloc[0][DC_CRAFTED_IN]
                }
            return attributes
        else:
            raise ValueError("Item not found in the data frame")

    def get_input_materials(self)->list:
        '''
        This function returns all input materials required as a dictionary
        '''
        return self.attributes.get("input_materials", [])

    def get_output_materials(self)->dict:
        '''
        This function returns all the output materials
        Note: In some cases additional outputs come out
        '''
        return {
            "output_material": self.attributes.get("name"),
            "output_qty": self.attributes.get("output_qty"),
            "output_unit": self.attributes.get("output_unit"),
            "extra_item": self.attributes.get("extra_item"),
            "extra_item_qty": self.attributes.get("extra_item_qty"),
            "extra_item_unit": self.attributes.get("extra_item_unit")
        }

    def get_input_item_per_min(self)->dict:
        '''
        This function calculates the input items per minute
        '''
        pass

    def get_output_item_per_min(self)->dict:
        '''
        This function calculates the output items per minute
        '''
        pass
    
    def get_production_facility(self)->str:
        '''
        This function returns the crafting facility of the item
        '''
        self.attributes['production_facility']

    def __str__(self):
        return f"{self.name}: {self.attributes}"