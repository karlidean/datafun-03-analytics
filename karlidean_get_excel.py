"""
This example file fetches an Excel file from the web 
and saves it to a local file named sales.xlsx in a folder named karlidean_data.

Please save a copy of the provided utils_logger.py file 
in the same folder as this file.
"""

#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Import from external packages
import requests

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Import local modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

FETCHED_DATA_DIR = "karlidean_data"

#####################################
# Define Functions
#####################################

def fetch_excel_file(folder_name: str, filename: str, url: str) -> None:
    """
    Fetch Excel data from the given URL and write it to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        url (str): URL of the Excel file to fetch.

    Returns:
        None

    Example:
        fetch_excel_file("data", "data.xlsx", "https://example.com/data.xlsx")
    """
    if not url:
        logger.error("The URL provided is empty. Please provide a valid URL.")
        return

    try:
        logger.info(f"Fetching Excel data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        write_excel_file(folder_name, filename, response.content)
        logger.info(f"SUCCESS: Excel file fetched and saved as {filename}")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")

def write_excel_file(folder_name: str, filename: str, binary_data: bytes) -> None:
    """
    Write Excel binary data to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        binary_data (bytes): Binary content of the Excel file.

    Returns:
        None
    """
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        logger.info(f"Writing Excel data to {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('wb') as file:
            file.write(binary_data)
        logger.info(f"SUCCESS: Excel data written to {file_path}")
    except IOError as io_err:
        logger.error(f"Error writing Excel data to {file_path}: {io_err}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate fetching Excel data.
    """
    excel_url = 'https://www.w3resource.com/python-exercises/pandas/excel/SaleData.xlsx'
    logger.info("Starting Excel fetch demonstration...")
    fetch_excel_file(FETCHED_DATA_DIR, "sales.xlsx", excel_url)

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()