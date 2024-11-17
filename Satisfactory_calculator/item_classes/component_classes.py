### Here are the attributes of the items setup in a class
### This class might need to be refactored using property

from common.constants import *
from calculations.calculations import item_per_minute
from common.read_item_list import get_item_row
from common.common_checks import check_overclock
from calculations.calculations import overclock_factor
from calculations.calculations import number_of_machines

import pandas as pd

from item_classes.logistic_classes import Logistics
from common.error_logs import ErrorLogger

class Item:
    def __init__(self,name:str,item_type:str,overclock:float,data_frame:pd.DataFrame,logger:ErrorLogger) -> None:
        self.name = name
        self.item_type = item_type
        self.overclock = check_overclock(overclock)
        self.data_frame = data_frame
        self.logger = logger
        self.attributes = self._find_item()
    
    def _find_item(self) -> dict:
        '''
        Searches the data frame for the requested item and type and assigns attributes.
        '''
        item_row = get_item_row(self.data_frame,DC_ITEM,self.name,DC_ITEM_TYPE,self.item_type,DS_COMP)

        if item_row is not None:
            attributes = {
                **self._extract_basic_attributes(item_row),
                "input_materials": self._extract_input_materials(item_row)
            }
        
            # Conditionally add extra item details if they exist
            extra_item = self._extract_extra_item(item_row)
            if extra_item:
                attributes.update(extra_item)
        
            # Add production facility if available
            attributes["production_facility"] = item_row.get(DC_CRAFTED_IN, None)
            return attributes
        else:
            error_message = "Item not found in the data frame"
            if self.logger:
                self.logger.log_error(error_message)
            raise ValueError(error_message)

    def _extract_basic_attributes(self, item_row) -> dict:
        ''' Extracts core attributes like name, output quantity, and craft time. '''
        return {
            "name": self.name,
            "type": self.item_type,
            "output_qty": item_row.get(DC_ITEM_QTY, 0),
            "output_unit": item_row.get(DC_ITEM_QTY_UNIT, None),
            "craft_time": item_row.get(DC_CRAFT_TIME, 1)/overclock_factor(self.overclock),
            "craft_time_unit": item_row.get(DC_CRAFT_TIME_UNIT, None)
        }

    def _extract_input_materials(self, item_row) -> list:
        ''' Extracts input materials, handling missing materials gracefully. '''
        input_materials = []

        material_keys = [DC_INPUT_MAT_1, DC_INPUT_MAT_2, DC_INPUT_MAT_3, DC_INPUT_MAT_4]
        quantity_keys = [DC_INPUT_QTY_1, DC_INPUT_QTY_2, DC_INPUT_QTY_3, DC_INPUT_QTY_4]
        unit_keys = [DC_INPUT_QTY_UNIT_1, DC_INPUT_QTY_UNIT_2, DC_INPUT_QTY_UNIT_3, DC_INPUT_QTY_UNIT_4]

        for material_key, quantity_key, unit_key in zip(material_keys, quantity_keys, unit_keys):
            material = item_row.get(material_key, None)
            if pd.notna(material):  # Only add non-null materials
                input_materials.append({
                    "material": material,
                    "quantity": item_row.get(quantity_key, 0),
                    "unit": item_row.get(unit_key, None)
                })
        return input_materials

    def _extract_extra_item(self, item_row) -> dict:
        ''' Extracts extra item details if they exist. '''
        extra_item = item_row.get(DC_EXTRA_ITEM, None)
        if pd.notna(extra_item):
            return {
                "extra_item": extra_item,
                "extra_item_qty": item_row.get(DC_EXTA_ITEM_QTY, 0),
                "extra_item_unit": item_row.get(DC_EXTA_ITEM_UNIT, None)
            }
        return {}

    def get_input_materials(self)->dict:
        '''
        This function returns all input materials required as a dictionary
        '''
        return self.attributes.get("input_materials", {})

    def get_output_materials(self) -> dict:
        '''
        This function returns all the output materials.
        '''
        # Initializing a default return
        if not all(key in self.attributes for key in ["name", "output_qty", "output_unit"]):
            return {}  # Return an empty dictionary if any of the essential keys are missing
        
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
        # Initializing a default return
        if "input_materials" not in self.attributes:
            return {}  # Return an empty dictionary if any of the essential keys are missing
        
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
        # Initializing a default return
        if "output_qty" not in self.attributes or "craft_time" not in self.attributes:
            return None
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

    def _get_belt_type_in(self, req_rate:float)->dict:
        '''
        This function determines the required belt type
        '''       
        # Finds the required belts and returns its name and capcity
        belt_type = Logistics(self.data_frame,req_rate,self.logger)
        return {"name":belt_type.log_name,
                "capacity":belt_type.log_capacity,
                "num_belts":belt_type.no_belts
                }
   
    def get_belt_type_in_name(self, req_rate: float) -> str:
        '''
        Returns the name of the required belt type for the given rate.
        '''
        return self._get_belt_type_in(req_rate)["name"]

    def get_belt_type_in_capacity(self, req_rate: float) -> float:
        '''
        Returns the capacity of the required belt type for the given rate.
        '''
        return self._get_belt_type_in(req_rate)["capacity"]

    def get_belt_type_in_num_belts(self, req_rate: float) -> int:
        '''
        Returns the number of belts required for the given rate.
        '''
        return self._get_belt_type_in(req_rate)["num_belts"]

    def _get_belt_type_out(self, req_rate:float)->str:
        '''
        This function determines the required belt type for the output
        '''      
        # Calculate the belt rate required
        req_machines = number_of_machines(self.get_output_item_per_min(),req_rate)
        updated_req_rate = req_rate/req_machines
        
        # Finds the required belts and returns its name and capacity
        belt_type = Logistics(self.data_frame,updated_req_rate,self.logger)
        return {"name":belt_type.log_name,
                "capacity":belt_type.log_capacity,
                "num_belts":belt_type.no_belts
                }
    
    def get_belt_type_out_name(self, req_rate: float) -> str:
        '''
        Returns the name of the required belt type for the given rate.
        '''
        return self._get_belt_type_out(req_rate)["name"]

    def get_belt_type_out_capacity(self, req_rate: float) -> float:
        '''
        Returns the capacity of the required belt type for the given rate.
        '''
        return self._get_belt_type_out(req_rate)["capacity"]

    def get_belt_type_out_num_belts(self, req_rate: float) -> int:
        '''
        Returns the number of belts required for the given rate.
        '''
        return self._get_belt_type_out(req_rate)["num_belts"]

    def get_data_frame(self)->pd.DataFrame:
        '''
        This function returns the data frame
        '''
        return self.data_frame

    def __str__(self):
        return f"{self.name}: {self.attributes}"