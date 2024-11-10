# This is the main file of the calculator

# TODO: Do the remaining classes for the other sheets

# Importing packages
import pandas as pd

# Importing functions
from calculations.calculations import number_of_machines
from calculations.calculations import amount_of_power
from calculations.calculations import item_per_minute
from calculations.calculations import amount_of_power_gen

from item_classes.component_classes import Item
from item_classes.building_classes import Buildings
from item_classes.power_classes import PowerGenerator

# Importing constants
from common.constants import *


# Define what is requested
requested_item = 'Screw'
requested_item_type = 'Original'
requested_qty = 120  # pcs/min

# Define the power generation
requested_power = 'Coal Generator'
requested_fuel_type = 'Coal'

# Reading the file
dfs = pd.read_excel("item_list.xlsx", sheet_name=DS_SHEETS)

# Power generator class created
power_use = PowerGenerator(requested_power, requested_fuel_type, dfs)

# The request items are now given a class
screw_item = Item(requested_item, requested_item_type, dfs)

# Building class created
build_use = screw_item.get_production_facility()
build_item = Buildings(build_use,dfs)

# Requirement calculations done
req_machines = number_of_machines(screw_item.get_output_item_per_min(),requested_qty)
req_power = amount_of_power(build_item.get_power_use(),req_machines)
req_power_gen = amount_of_power_gen(req_power,power_use.get_power_gen())

# Get various attributes
# print("Input Materials:", screw_item.get_input_materials())
# print("Output Materials:", screw_item.get_output_materials())
# print("Input Items per Minute:", screw_item.get_input_item_per_min())
# print("Output Item per Minute:", screw_item.get_output_item_per_min())
# print("Production Facility:", screw_item.get_production_facility())

print("-----------------------------")
print("Required number of machines:",req_machines)
print("Required amount of power for ", req_machines, screw_item.get_production_facility(),": ",req_power,build_item.get_power_unit())
print("Required number of ", requested_power, " using ",requested_fuel_type, " as fuel: ", req_power_gen)


# # Finding the item use and its sheet
# item_use = find_item(dfs,requested_item,requested_item_type)
# sheet_name = next(iter(item_use))

# # Setting the dictionary to a current use dictionary
# current_item = item_use[sheet_name]

# # Updating the item_use dictionary with items/min
# current_item = item_per_minute(current_item)

# # Finding the required building to manufacture in
# req_building = current_item[DC_CRAFTED_IN]
# building_use = find_item(dfs,req_building)
# sheet_name = next(iter(building_use))
# current_building = building_use[sheet_name]

# # Calculating the required amounts
# req_machines = number_of_machines(current_item,requested_qty)
# req_power = amount_of_power(current_building,req_machines)

# # Printing the results
# print(f'You requested {requested_qty} pcs of {requested_item_type} {requested_item}.\n It will require {req_machines} of {req_building} and {req_power} {DC_POWER_UNIT} ')

# print('-----------------')
# for sheet, details in item_use.items():
#     print(f"{sheet}:")  # Print the main sheet name/key
#     for key, value in details.items():
#         print(f"  {key}: {value}\n")  # Indent for clarity
