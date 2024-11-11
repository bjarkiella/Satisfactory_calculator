# This file contains all the calculation function required

# Importing Constants
from common.constants import *
import math as m

def number_of_machines(production_rate:float,qty:float)->float:
    '''
    This function calculates the number of machines required for desired output
    '''
    
    return max(1.0, round(qty/production_rate,2))

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
    return max(1.0, round(power_required / power_gen,2))

def overclock_factor(value:float)->float:
    '''
    This function returns an overclock value
    '''
    return value/100.0

def overclock_power(value:float)->float:
    '''
    This function calculates the overclock factor on power consumption of a building
    '''
    return round(m.pow(value/100.0,1.321928),5)