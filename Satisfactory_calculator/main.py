# This is the main file of the calculator

# Importing packages
import pandas as pd
import math as m

# Importing functions
from calculations.calculations import number_of_machines
from calculations.calculations import amount_of_power
from calculations.calculations import amount_of_power_gen

from item_classes.component_classes import Item
from item_classes.building_classes import Buildings
from item_classes.power_classes import PowerGenerator
from item_classes.production_classes import ProductionLine

from common.error_logs import ErrorLogger

# Importing constants
from common.constants import *

# Initializing the error log
logger = ErrorLogger()

# Define what is requested
requested_item = 'Screw'
requested_item_type = 'Original'
# requested_item = 'Biomass'
# requested_item_type = 'Wood'
requested_qty = 120  # pcs/min
requested_item_overclock = 100 # Overclock in %, min 1% max 250%

# Define the power generation
requested_power = 'Coal Generator'
requested_fuel_type = 'Coal'
requested_power_overclock = 100  # Overclock in %

# Reading the file
dfs = pd.read_excel("item_list.xlsx", sheet_name=DS_SHEETS)

# Power generator class created
power_use = PowerGenerator(requested_power, requested_fuel_type, requested_power_overclock, dfs, logger)

# The request items are now given a class
req_item = Item(requested_item, requested_item_type, requested_item_overclock, dfs, logger)

# Building class created
build_use = req_item.get_production_facility()
build_item = Buildings(build_use,requested_item_overclock,dfs, logger)

# Requirement calculations done
req_machines = number_of_machines(req_item.get_output_item_per_min(),requested_qty)
req_power = amount_of_power(build_item.power_use,req_machines)
req_power_gen = amount_of_power_gen(req_power,power_use.get_power_gen())

# Logstics calculations done
type_in_belt = req_item.get_belt_type_in_name(requested_qty)
no_in_belt = req_item.get_belt_type_in_num_belts(requested_qty)
type_out_belt = req_item.get_belt_type_out_name(requested_qty)
no_out_belt = req_item.get_belt_type_out_num_belts(requested_qty) 

# Production line calculations
production_line = ProductionLine(req_item,requested_qty,requested_item_overclock, logger)

print("-------- Item request --------")
print("Requested item: ", req_item.name," and type: ",req_item.item_type)
print("Requested qty: ", requested_qty)
print("Requested overlock: ", requested_item_overclock,"%")

print("--------- Required Inputs ---------")
print("Required input items:",req_item.get_input_item_per_min())

print(' ')
print("-------- Power Generation --------")
print("Requested power generator: ", power_use.name, " and type: ",power_use.fuel_type)
print("Requested power overclock: ", requested_power_overclock, "%")

print(' ')
print("--------- Required Machines ---------")
print("Required number of machines:",req_machines)
print("Required amount of power for ", req_item.get_production_facility(),": ",req_power,build_item.power_unit)
print("Required number of ", requested_power, " using ",requested_fuel_type, " as fuel: ", req_power_gen)
print("Generated power ", power_use.get_power_gen(),power_use.get_power_gen_unit())

print(' ')
print("--------- Required Logistics ---------")
print("Required belt type for input:",no_in_belt,"off type",type_in_belt)
print("Required belt type for output:",m.ceil(req_machines),"off type",type_out_belt)

print(' ')
print("--------- Full production line ---------")
production_line.print_requirements()

print(' ')
print("--------- Debug check ---------")
print(req_item.get_output_item_per_min())
