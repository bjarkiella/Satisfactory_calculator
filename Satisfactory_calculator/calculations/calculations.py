# This file contains all the calculation function required

# Importing Constants
from common.constants import DATA_COLUMN_CRAFT_TIME
from common.constants import DATA_COLUMN_POWER_USE

def number_of_machines(item:dict,qty:int)->float:
    '''
    This function calculates the number of machines required for desired output
    '''
    
    return qty/item[DATA_COLUMN_CRAFT_TIME]

def amount_of_power(item:dict,no_machines:float)->float:
    '''
    This function calculates the total power consumptions of the machines
    '''
    return item[DATA_COLUMN_POWER_USE]*no_machines
