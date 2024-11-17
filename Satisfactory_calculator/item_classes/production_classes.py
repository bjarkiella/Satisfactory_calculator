# This file contains a class that breaks down the production line of an Item and Buildings objects

from item_classes.component_classes import Item
from item_classes.building_classes import Buildings
from calculations.calculations import number_of_machines
from common.constants import *

from common.error_logs import ErrorLogger


class ProductionLine:

    def __init__(self, item: Item, target_output_rate: float, overclock: float, logger: ErrorLogger):
        self.item = item
        self.target_output_rate = target_output_rate
        self.overclock = overclock
        self.default_type = DC_DEFAULT_ITEM_TYPE
        self.default_overclock = 100.0
        self.data_frame = self.item.get_data_frame()
        self.logger = logger
        self.building = Buildings(self.item.get_production_facility(),self.overclock,self.data_frame,self.logger)
        self.requirements = self._calculate_requirements()
        

    def _calculate_requirements(self):
        '''
        This function initiates the recursive iteration
        '''
        # Start the recursive calculation for the item
        return self._calculate_item_requirements(self.item, self.target_output_rate, self.overclock)      

    def _calculate_item_requirements(self, item: Item, req_output_rate: float, overclock: float, depth: int = 0, max_depth:int = 10):
        '''
        This function iterates down through the input materials and stores the Item and Building information. Max depth set to 10
        '''
        if depth > max_depth:
            warning_message = f"Maximum recursion depth ({max_depth}) exceeded. Check for circular dependencies or invalid input data."
            if self.logger:
                self.logger.log_error(warning_message)
            raise RecursionError(warning_message)
        
        # Calculate the number of machines needed for the given output rate and overclock
        machine_count = number_of_machines(item.get_output_item_per_min(),req_output_rate)
        
        # Create a Buildings object for this item
        building = Buildings(item.get_production_facility(), overclock, self.data_frame, self.logger)
        
        # Get the input materials for this item
        input_materials = item.get_input_materials()
        
        # Initialize totals for required inputs and energy
        total_energy = machine_count * building.power_use
        requirements = {"production":item.get_production_facility(),"machines": machine_count, "energy": total_energy, "inputs": {}}
        
        # Loop through each input material and calculate recursively
        for input_material in input_materials:
            try:
                input_item = Item(input_material["material"], self.default_type, self.default_overclock, self.data_frame,self.logger)  # Initialize Item for each input
                input_building = Buildings(input_item.get_production_facility(),self.default_overclock, self.data_frame,self.logger)
            except ValueError:
                requirements["inputs"][input_material["material"]] = {"error": "Item not found"}
                continue

            input_rate = input_material["quantity"] * requirements.get("machines")  # Total input needed
            input_requirements = self._calculate_item_requirements(input_item, input_rate, self.default_overclock,depth+1)
            requirements["inputs"][input_material["material"]] = input_requirements
        return requirements

    def print_requirements(self):
        '''
        Prints the production requirements in a readable format.
        '''
        if self.requirements is None:
            print("No requirements calculated yet. Please call calculate_requirements() first.")
        else:
            self._print_requirements_recursive(self.requirements)

    def _print_requirements_recursive(self, requirements, level=0):
        '''
        Helper function to recursively print the requirements.
        '''
        indent = "  " * level  # Create indentation based on the recursion level

        # Print the current item’s production details
        print(f"{indent}Production Facility: {requirements.get('production', 'Unknown')}")
        print(f"{indent}  Machines Required: {requirements.get('machines', 0)}")
        print(f"{indent}  Total Energy: {requirements.get('energy', 0):.2f} MW")

        # Print input materials, if any
        if 'inputs' in requirements and requirements['inputs']:
            print(f"{indent}  Input Materials:")
            for material, input_req in requirements['inputs'].items():
                print(f"{indent}    - {material}:")
                self._print_requirements_recursive(input_req, level + 2)  # Recursive call for nested inputs

        return requirements
