'''
This file will fetch a CSV file from the web /
and saves it to a local file named 2019_NCAA_Womens_Volleyball.csv in a folder named karlidean_data

For the best results, I have added the file utils_logger.py from the example repo
to the same folder as this file.
'''

#######################
# Importing Modules at the top
#######################

# Importing from Python Standard Library
import pathlib
import sys

# Importing from external packages
import requests

# Ensuring project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Importing local modules
from utils_logger import logger

#######################
# Declaring Global Variables
#######################

FETCHED_DATA_DIR = "karlidean_data"

#######################
# Defining Functions
#######################

def fetch_csv_file(folder_name: str, filename: str, url: str) -> None:
    '''
    This piece fetches CSV data from the given URL and writes it to a file.
    
    Args:
        folder_name (str): Name of the folder to save the file
        filename (str): Name of the output file
        url (str): URL of the csv file to fetch
        
    Returns:
        None
    
    Example:
        fetch_csv_file("data", "data.csv", "https://example.com/csv")
    '''
    if not url:
        logger.error("The URL provided is empty. Please provide a valid URL.")
        return
    
    try:
        logger.info(f"Fetching CSV data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        write_csv_file(folder_name, filename, response.text)
        logger.info(f"SUCCESS: CSV file fetched and saved as {filename}")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")

def write_csv_file(folder_name: str, filename: str, string_data: str) -> None:
    '''
    This piece writes CSV data to a file.
    
    Args:
        folder_name (str): Name of the folder to save the file
        filename (str): Name of the output file
        string_data (str): CSV content as a string
        
    Returns:
        None
    '''

    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        logger.info(f"Writing CSV data to {file_path}")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            file.write(string_data)
        logger.info(f"SUCCESS: CSV data written to {file_path}")
    except IOError as io_err:
        logger.error(f"Error has occurred writing CSV data to {file_path}: {io_err}")

#######################
# Defining main() function
#######################

def main():
    '''
    Main function to demonstrate fetching CSV data
    '''

    csv_url = 'https://raw.githubusercontent.com/openvolley/R_workshop_2022/refs/heads/master/example_data/NCAA_D1W_2019.csv'
    logger.info("Starting CSV fetch demonstration...")
    fetch_csv_file(FETCHED_DATA_DIR, "2019_NCAA_Womens_Volleyball.csv", csv_url)

#######################
# Conditional Execution
#######################

if __name__ == '__main__':
    main()