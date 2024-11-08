# This file contains all the calculation function required

# Importing Constants
from common.constants import *


def number_of_machines(production_rate:float,qty:float)->float:
    '''
    This function calculates the number of machines required for desired output
    '''
    
    return qty/production_rate

# def number_of_machines(item:dict,qty:int)->float:
#     '''
#     This function calculates the number of machines required for desired output
#     '''
    
#     return qty/item[DC_ITEM_PER_MIN]

def amount_of_power(item:dict,no_machines:float)->float:
    '''
    This function calculates the total power consumptions of the machines
    '''
    return item[DC_POWER_USE]*no_machines

def item_per_minute(production_qty:float,craft_time:float)->float:
    '''
    This function returns item per minute
    '''
    return production_qty * 60 / craft_time

# def item_per_minute(item:dict)->dict:
#     '''
#     This function calculates the items per minute for request item
#     '''
#     # Initilizing
#     no_inputs = len([key for key in globals() if key.startswith(DC_INPUT_MAT)])
    
#     # Checking if craft_time column is present before calculating
#     if DC_CRAFT_TIME in (data_columns := item):
#         item['item_per_min'] = item[DC_ITEM_QTY] * float(60) / item[DC_CRAFT_TIME] 

#         # Calculating the input materials, if present
#         if DC_INPUT_MAT_1 in (data_columns := item):
#             for i in range(1,no_inputs + 1):
#                 mat_key = globals().get(f'{DC_INPUT_MAT}_{i}')
#                 qty_key = globals().get(f'{DC_INPUT_QTY}_{i}')
#                 per_min_key = f'input_{i}_per_min'
#                 if mat_key in data_columns and item.get(mat_key):
#                     item[per_min_key] = item[qty_key] * 60 / item[DC_CRAFT_TIME]
#                 else:
#                     item[per_min_key] = None

#     return item
