# This is the main file of the calculator

# TODO: Check on the craftting times and quantities, something is wrong there
# TODO: 

# Importing packages
import pandas as pd

# Importing functions
from calculations.calculations import number_of_machines
from calculations.calculations import amount_of_power
from common.read_item_list import find_item

# Importing constants
from common.constants import DATA_SHEET_BUILD
from common.constants import DATA_COLUMN_CRAFTED_IN
from common.constants import DATA_COLUMN_POWER_UNIT

# Define what is requested
requested_item = 'Screw'
requested_qty = 120

# Reading the file
dfs = pd.read_excel("item_list.xlsx", sheet_name=None)

# Finding the item use
item_use = find_item(dfs,requested_item)

# Finding the required building to manufacture in
req_building = item_use[DATA_COLUMN_CRAFTED_IN]
building_use = find_item(dfs,req_building)

# Calculating the required amounts
req_machines = number_of_machines(item_use,requested_qty)
req_power = amount_of_power(building_use,req_machines)

# Printing the results
print(f'You requested {requested_qty} pcs of {requested_item}.\n It will require {req_machines} of {req_building} and {req_power} {DATA_COLUMN_POWER_UNIT} ')
