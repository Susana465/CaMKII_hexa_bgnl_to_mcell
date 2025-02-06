import os
from prepare_run_files import prepare_out_folder
# Call the function "set_up_model" that runs mcell model with params specs from mcell_params.py
from mcell_params import set_up_model, process_parameters

def run_model(parameter_overrides=None, bngl_file="dodecamer.bngl"):
    """
    Runs the MCell model with optional parameter overrides.

    Args:
        parameter_overrides: Optional dictionary of parameters to override.
        bngl_file: Name of the BNGL file to load.
        
    Returns:
        Tuple containing the run folder path, timestamp, and processed parameters DataFrame.
    """

    # Set up the model described in mcell_params.py under the function set_up_model()
    model = set_up_model()

    # Define MCell parameter files
    mcell_param_file = "mcell_params.py"

    # Call the function and capture the path to the run folder and timestamp
    run_folder, timestamp = prepare_out_folder("data_output", model.config.seed, files_to_copy=[bngl_file, mcell_param_file])

    # This wont run now, will run if set to True. Save viz_data under timestamped folder
    if False:
        viz_output = m.VizOutput(
            os.path.join(run_folder, f"viz_data/Scene_"),
            every_n_timesteps=100
        )
        model.add_viz_output(viz_output)

    #  If no overrides are provided, 
    #  passing an empty dictionary ensures the model behaves as it would without any overrides.
    if parameter_overrides is None:
        parameter_overrides = {}

    # Load the BNGL file and apply the parameter overrides
    model.load_bngl(
        os.path.join(run_folder, bngl_file), 
        observables_path_or_file=os.path.join(run_folder, f"{timestamp}_out.gdat"),
        parameter_overrides=parameter_overrides
    )

    # Specifies periodicity of visualization output
    for count in model.counts:
        count.every_n_timesteps = 5000

    # Process the parameters and save them to CSV
    ITERATIONS, df = process_parameters(bngl_file, run_folder, timestamp, parameter_overrides)

    # Check to see if total iterations is defined as a global parameter
    if ITERATIONS is None:
        ITERATIONS = 100

    # Set the total iterations (use the ITERATIONS from the BNGL or the overridden one)
    model.config.total_iterations = ITERATIONS

    # Initialize, export, and run the model
    model.initialize()
    model.run_iterations(ITERATIONS)
    model.end_simulation()

    return run_folder, timestamp, df

if __name__ == "__main__":
    run_model()  # This will only run if run_model.py is executed directly, not when importing the script into other files.