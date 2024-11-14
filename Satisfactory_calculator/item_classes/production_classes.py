# This file contains a class that breaks down the production line of an Item object
# TODO: Need to fix this one. The idea is that:
#  1. the original Item is sent here and 
#  2. Then looped through a function in this class 
#  3. It should keep track of the number of production facilites for each produced Item
#  4. It should keep track of total amount of power required for each Item
#  5. Until no the input item cannot be found as an Item

from item_classes.component_classes import Item
from calculations.calculations import number_of_machines


class ProductionLine:
    def __init__(self, item: Item, target_output_rate: float, overclock: float = 100.0):
        self.item = item
        self.target_output_rate = target_output_rate
        self.overclock = overclock

    def calculate_requirements(self):
        # Start the recursive calculation for the item
        return self._calculate_item_requirements(self.item, self.target_output_rate, self.overclock)

    def _calculate_item_requirements(self, item: Item, output_rate: float, overclock: float):
        # Calculate the number of machines needed for the given output rate and overclock
        machine_count = number_of_machines(output_rate)
        machine_count = self._calculate_machines_needed(item, output_rate, overclock)  # THIS CAN REFER TO CALCULATION SHEET
        
        # Get the input materials for this item
        input_materials = item.get_input_materials()
        
        # Initialize totals for required inputs and energy
        total_energy = machine_count * item.attributes["power_use"]
        requirements = {"machines": machine_count, "energy": total_energy, "inputs": {}}
        
        # Loop through each input material and calculate recursively
        for input in input_materials:
            input_item = Item(input["material"], ...)  # Initialize Item for each input
            input_rate = input["quantity"] * machine_count  # Total input needed
            input_requirements = self._calculate_item_requirements(input_item, input_rate, overclock)
            requirements["inputs"][input["material"]] = input_requirements

        return requirements

    # def _calculate_machines_needed(self, item: Item, output_rate: float, overclock: float) -> int:
    #     # Calculate the per-minute output of the item based on overclock
    #     per_min_output = item.get_output_item_per_min() * (overclock / 100)
    #     # Determine how many machines are needed to meet the target output rate
    #     return int(output_rate / per_min_output) + (1 if output_rate % per_min_output != 0 else 0)
