"""
This example file fetches a text file of Genesis from the Bible from the web 
and saves it to a local file named genesis.txt in a folder named karlidean_data.

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

def fetch_txt_file(folder_name: str, filename: str, url: str) -> None:
    """
    Fetch text data from the given URL and write it to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        url (str): URL of the text file to fetch.

    Returns:
        None

    Example:
        fetch_txt_file("data", "romeo.txt", "https://example.com/romeo.txt")
    """
    if not url:
        logger.error("The URL provided is empty. Please provide a valid URL.")
        return

    try:
        logger.info(f"Fetching text data from {url}...")
        response = requests.get(url)
        response.raise_for_status()
        write_txt_file(folder_name, filename, response.text)
        logger.info(f"SUCCESS: Text file fetched and saved as {filename}")
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")

def write_txt_file(folder_name: str, filename: str, string_data: str) -> None:
    """
    Write text data to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        string_data (str): Text content to write to the file.

    Returns:
        None
    """
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        logger.info(f"Writing data to {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            file.write(string_data)
        logger.info(f"SUCCESS: Data written to {file_path}")
    except IOError as io_err:
        logger.error(f"Error writing to file {file_path}: {io_err}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate fetching text data.
    """
    txt_url = 'https://people.sc.fsu.edu/~jburkardt/datasets/text/genesis.txt'
    logger.info("Starting text fetch demonstration...")
    fetch_txt_file(FETCHED_DATA_DIR, "genesis.txt", txt_url)

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()