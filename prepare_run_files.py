# This is the script where I prepare folders to save model runs
import os
from datetime import datetime
import shutil  # for easier file copying

def prepare_out_folder(folder_name, seed, files_to_copy=["file.bngl", "file.py"]):
    
    # Generate the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = os.path.join(folder_name, f"run_{timestamp}_seed_{seed}")

    # Create the timestamped folder
    os.makedirs(folder_name)

    # Loop over each file and copy it to the destination folder
    for file_name in files_to_copy:
        dest_file = os.path.join(folder_name, file_name)  # Destination path with original name
        shutil.copy(file_name, dest_file)  # Copy the file with original name
    
    print(f"New run, files will be saved in {folder_name}.")

    return folder_name, timestamp

