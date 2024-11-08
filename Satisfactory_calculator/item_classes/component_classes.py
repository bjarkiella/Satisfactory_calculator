### Here are the attributes of the items setup in a class


from common.constants import *
from calculations.calculations import item_per_minute

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
                "name": item_row.iloc[0].get(DC_ITEM, None),
                "output_qty": item_row.iloc[0].get(DC_ITEM_QTY, 0),
                "output_unit": item_row.iloc[0].get(DC_ITEM_QTY_UNIT, None),
                "craft_time": item_row.iloc[0].get(DC_CRAFT_TIME, 1),
                "craft_time_unit": item_row.iloc[0].get(DC_CRAFT_TIME_UNIT, None),
                "input_materials": [
                    {
                        "material": item_row.iloc[0].get(DC_INPUT_MAT_1, None),
                        "quantity": item_row.iloc[0].get(DC_INPUT_QTY_1, 0),
                        "unit": item_row.iloc[0].get(DC_INPUT_QTY_UNIT_1, None)
                    }
                ]
            }

            # Add additional input materials only if they exist
            for i in range(2, 5):  # For DC_INPUT_MAT_2 to DC_INPUT_MAT_4
                material = item_row.iloc[0].get(f"{DC_INPUT_MAT}_{i}", None)
                if pd.notna(material):  # Add only non-null materials
                    attributes["input_materials"].append({
                        "material": material,
                        "quantity": item_row.iloc[0].get(f"{DC_INPUT_QTY}_{i}", 0),
                        "unit": item_row.iloc[0].get(f"{DC_INPUT_QTY_UNIT}_{i}", None)
                    })

            # Conditionally add extra_item fields if available
            extra_item = item_row.iloc[0].get(DC_EXTRA_ITEM, None)
            if pd.notna(extra_item):
                attributes.update({
                    "extra_item": extra_item,
                    "extra_item_qty": item_row.iloc[0].get(DC_EXTA_ITEM_QTY, 0),
                    "extra_item_unit": item_row.iloc[0].get(DC_EXTA_ITEM_UNIT, None)
                })

            # Add production facility attribute
            attributes["production_facility"] = item_row.iloc[0].get(DC_CRAFTED_IN, None)

            return attributes
        else:
            raise ValueError("Item not found in the data frame")

    def get_input_materials(self)->dict:
        '''
        This function returns all input materials required as a dictionary
        '''
        return self.attributes.get("input_materials", {})

    def get_output_materials(self) -> dict:
        '''
        This function returns all the output materials.
        '''
        # Initialize output dictionary with basic output materials
        out_dict = {
            "output_material": self.attributes.get("name"),
            "output_qty": self.attributes.get("output_qty"),
            "output_unit": self.attributes.get("output_unit")
        }

        # Add extra item information if it exists
        if "extra_item" in self.attributes:
            out_dict.update({
                "extra_item": self.attributes["extra_item"],
                "extra_item_qty": self.attributes["extra_item_qty"],
                "extra_item_unit": self.attributes["extra_item_unit"]
            })

        return out_dict

    def get_input_item_per_min(self) -> dict:
        '''
        This function calculates the input items per minute.
        '''
        # Initialize the dictionary to store per-minute rates of each input material
        out_dict = {}

        # Loop over each input material in the list
        for idx, material in enumerate(self.attributes.get("input_materials", []), start=1):
            # Calculate the per-minute rate for each material
            per_min_qty = item_per_minute(material["quantity"], self.attributes.get("craft_time"))
        
            # Store the result in the dictionary using material names or indices as keys
            out_dict[f"input_material_{idx}"] = {
                "material": material["material"],
                "quantity_per_min": per_min_qty
            }
        return out_dict

    def get_output_item_per_min(self) -> float:
        '''
        This function calculates the output items per minute.
        '''

        return item_per_minute(self.attributes.get("output_qty"), self.attributes.get("craft_time"))

    def get_extra_output_item_per_min(self) -> float:
        '''
        This function calculates the per-minute rate of the extra output item.
        Returns None if there is no extra output item.
        '''
        # Check if extra item exists in the attributes
        if "extra_item" not in self.attributes:
            return None

        # Calculate and return the per-minute rate for the extra item
        return item_per_minute(self.attributes.get("extra_item_qty"), self.attributes.get("craft_time"))


    def get_production_facility(self)->str:
        '''
        This function returns the crafting facility of the item
        '''
        return self.attributes.get("production_facility", None)

    def __str__(self):
        return f"{self.name}: {self.attributes}"