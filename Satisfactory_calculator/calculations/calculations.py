# This file contains all the calculation function required

# Importing Constants
from common.constants import *
import math as m

def number_of_machines(production_rate:float,qty:float)->float:
    '''
    This function calculates the number of machines required for desired output
    '''
    
    return qty/production_rate

def amount_of_power(power_use:float,no_machines:float)->float:
    '''
    This function calculates the total power consumptions of the machines
    '''
    return power_use*no_machines

def item_per_minute(production_qty:float,craft_time:float)->float:
    '''
    This function returns item per minute
    '''
    return production_qty * 60 / craft_time

def amount_of_power_gen(power_required:float,power_gen:float)->float:
    '''
    This function returns the amount of power generator required to fulfill power demand
    '''
    return max(1.0, m.ceil(power_required / power_gen))

def overclock_factor(value:float)->float:
    '''
    This function returns an overclock value
    '''
    return value/100.0