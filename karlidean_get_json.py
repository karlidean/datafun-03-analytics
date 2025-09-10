"""
This example file fetches JSON data of the stars in the night sky, with their names, type, and position.
from the web and saves it to a local file named star.json in karlidean_data.

"""

#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import json
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

def fetch_json_file(folder_name: str, filename: str, url: str) -> None:
    """
    Fetch JSON data from the given URL and write it to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        url (str): URL of the JSON file to fetch.

    Returns:
        None

    Example:
        fetch_json_file("data", "data.json", "https://example.com/data.json")
    """
    if not url:
        logger.error("The URL provided is empty. Please provide a valid URL.")
        return

    try:
        logger.info(f"Fetching JSON data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        write_json_file(folder_name, filename, response.json())
        logger.info(f"SUCCESS: JSON file fetched and saved as {filename}")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")

def write_json_file(folder_name: str, filename: str, json_data: dict) -> None:
    """
    Write JSON data to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        json_data (dict): JSON data to write to the file.

    Returns:
        None
    """
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        logger.info(f"Writing JSON data to {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            json.dump(json_data, file, indent=4)
        logger.info(f"SUCCESS: JSON data written to {file_path}")
    except IOError as io_err:
        logger.error(f"Error writing JSON data to {file_path}: {io_err}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate fetching JSON data.
    """
    json_url = 'https://brettonw.github.io/YaleBrightStarCatalog/bsc5.json'
    logger.info("Starting JSON fetch demonstration...")
    fetch_json_file(FETCHED_DATA_DIR, "stars.json", json_url)

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()