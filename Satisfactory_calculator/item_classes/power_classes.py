### Here are the attributes of power generators

# TODO: Overclocker modifiers to be added here
from common.constants import *
from common.read_item_list import get_item_row
from common.common_checks import check_overclock
from calculations.calculations import overclock_factor

import pandas as pd

class PowerGenerator:
    def __init__(self,name:str,fuel_type:str,overclock:float,data_frame:pd.DataFrame) -> None:
        self.name = name
        self.fuel_type = fuel_type
        self.overclock = check_overclock(overclock)
        self.data_frame = data_frame
        self.attributes = self._find_power_gen()
    
    def _find_power_gen(self) -> dict:
        '''
        This function searches the data frame for the requested item and type and gives it the attributes
        '''
        
        power_gen_row = get_item_row(self.data_frame,DC_ITEM,self.name,DC_FUEL_TYPE,self.fuel_type,DS_POWER)

        if power_gen_row is not None:
            attributes = {
                **self._extract_basic_attributes(power_gen_row),
                "input_materials": self._extract_input_materials(power_gen_row)
            }
            return attributes
        else:
            raise ValueError("Item not found in the data frame")

    def _extract_basic_attributes(self, power_gen_row) -> dict:
        ''' Extracts core attributes like name, output quantity, and craft time. '''
        return {
            "name": self.name,
            "fuel_type": self.fuel_type,
            "power_gen": power_gen_row.get(DC_POWER_GEN, 0)*overclock_factor(self.overclock),
            "power_gen_unit": power_gen_row.get(DC_POWER_GEN_UNIT, None)
        }

    def _extract_input_materials(self, power_gen_row) -> list:
        ''' Extracts input materials, handling missing materials gracefully. '''
        input_materials = []
        for i in range(1, 2):  # For DC_POWER_INPUT_MAT_1 to DC_POWER_INPUT_MAT_2
            material = power_gen_row.get(f"{DC_POWER_INPUT_MAT}_{i}", None)
            if pd.notna(material):  # Only add non-null materials
                input_materials.append({
                    "material": material,
                    "quantity": power_gen_row.get(f"{DC_POWER_INPUT_QTY}_{i}", 0)*overclock_factor(self.overclock),
                    "unit": power_gen_row.get(f"{DC_POWER_INPUT_QTY_UNIT}_{i}", None)
                })
        return input_materials

    def get_input_materials(self)->dict:
        '''
        This function returns all input materials required as a dictionary
        '''
        return self.attributes.get("input_materials", {})

    def get_power_gen(self) -> float:
        '''
        This function returns the power generation of a given generator
        '''
        return self.attributes.get("power_gen", None)
    
    def get_power_gen_unit(self) -> float:
        '''
        This function returns the power generation of a given generator
        '''
        return self.attributes.get("power_gen_unit",None)