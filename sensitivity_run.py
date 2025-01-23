import os

from run_model import run_model

# different 'kon' values to run through
kon_values = [
    0.1, 0.5, 1, 5, 10,  # Filling low range gaps
    1e5, 1.5e5, 2e5, 2.5e5, 3e5, 4e5, 5e5, 6e5, 7.5e5, 1e6,  # Original range
    2e6, 3e6, 5e6, 7.5e6,  # Filling intermediate range
    2e8, 5e8, 7.5e8  # Filling high range
]
koff_values = [] 

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

parameter_sweep(kon_values, 'kon')

# Iterate over the kon values and run the model
# for kon in kon_values:
#     print(f"Starting run for kon = {kon}") 
#     parameter_overrides = {'kon': kon}
#     run_model(parameter_overrides)
#     print(f"Run completed for kon = {kon}")

# # Iterate over the kon values and run the model
# for koff in koff_values:
#     print(f"Starting run for koff = {koff}") 
#     parameter_overrides = {'koff': koff}
#     run_model(parameter_overrides)
#     print(f"Run completed for koff = {koff}")

# def run_multiple_parameters(param_names, param_values_list):
#     """
#     Run the model for each combination of parameters in param_values_list.

#     param_names: List of parameter names (e.g., ['kon', 'koff'])
#     param_values_list: List of lists, where each list contains values for one parameter

#     """
#     # Determine the number of iterations (assumes all lists have the same length)
#     for param_combination in zip(*param_values_list):
#         parameter_overrides = {param_names[i]: param_combination[i] for i in range(len(param_names))}
#         print(f"Starting run with parameters: {parameter_overrides}")
#         run_model(parameter_overrides)
#         print(f"Run completed with parameters: {parameter_overrides}")

# # Run the model for both kon and koff values
# run_multiple_parameters(['kon', 'koff'], [kon_values, koff_values])