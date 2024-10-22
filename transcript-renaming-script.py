import os
import logging
import pandas as pd
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename='folder_renaming.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load the EIN dictionary from the CSV file
csv_file_path = input("Enter the Dictionary: ").replace('"',"")  # I hate python at times, replacing " to fix bug from userinput
try:
    df = pd.read_csv(csv_file_path)
    ein_dict = pd.Series(df['Account Name'].values, index=df['SSN/EIN']).to_dict()  # Extracting Business Names and EINs
except Exception as e:
    logging.error(f"Error reading CSV file: {e}")
    raise

# Set the directory to search for folders
directory_path = input("Enter the directory to rename files: ").replace('"',"")  # I hate python at times, replacing " to fix bug from userinput

# Loop through the directory with a progress bar
for ein, business_name in tqdm(ein_dict.items(), desc="Processing Folders"):
    # Construct the path for the existing folder
    while(len(str(ein))<9): #Ensure EIN is a 9 char sequence
        ein = "0"+(str(ein)) 
    existing_folder_path = os.path.join(directory_path, str(ein)[:2] + '-' + str(ein)[2:])  # Convert int from excel to a 2-9 proper format EIN

    # Log the folder being checked
    logging.info(f'Checking for folder: "{existing_folder_path}"')
    
    # Check if the folder exists
    if os.path.isdir(existing_folder_path):
        # Create the new folder name
        trimmedCompName = "".join(x for x in business_name if x.isalnum() or x.isspace())
        target_folder_name = f"{trimmedCompName} EIN {ein}"
        new_folder_path = os.path.join(directory_path, target_folder_name)

        # Rename the folder
        os.rename(existing_folder_path, new_folder_path)
        log_message = f'Renamed "{existing_folder_path}" to "{new_folder_path}"'
        print(log_message)  # Print to console
        logging.info(log_message)  # Log to file
    else:
        log_message = f'Folder "{existing_folder_path}" does not exist.'
        print(log_message)  # Print to console
        logging.warning(log_message)  # Log to file

print("Folder renaming complete.")
