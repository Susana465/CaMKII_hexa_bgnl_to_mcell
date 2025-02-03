import os

from run_model import run_model

# different 'kon' values to run through
kon_values = [-10]

koff_values = [-10] 

# Note that if parameter_value does not match, this code currently will not throw an error and will just run with the preset value stated in the .bngl file. 
# Check the .csv of values to see which 'kon' was used


def parameter_sweep(values, parameter_name):
    """
    This (void) function does a parameter sweep by iterating over a list of values for a given parameter.

    It's primary goal is to perform an action (run model iteratively) rather than calculate and return a value.

    Arguments it takes:
    values (list): A list of values to sweep through for the specified parameter.
    parameter_name (str): The name of the parameter to override in each iteration.
    """
    for value in values:
        print(f"Starting run for {parameter_name} = {value}")
        parameter_overrides = {parameter_name: value}
        run_model(parameter_overrides)
        print(f"Run completed for {parameter_name} = {value}")

parameter_sweep(kon_values, 'kon_camkii_open')