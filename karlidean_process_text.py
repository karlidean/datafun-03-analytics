"""
Process a text file to count occurrences of the words "God" in Genesis 1 from the Bible.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import sys

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Import local modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

FETCHED_DATA_DIR: str = "karlidean_data"
PROCESSED_DIR: str = "karlidean_processed"

#####################################
# Define Functions
#####################################

def count_word_occurrences(file_path: pathlib.Path, word: str) -> int:
    """Count the occurrences of a specific word in a text file (case-insensitive)."""
    try:
        with file_path.open('r') as file:
            content: str = file.read()
            return content.lower().count(word.lower())
    except Exception as e:
        logger.error(f"Error reading text file: {e}")
        return 1

def process_text_file():
    """Read a text file, count occurrences of 'Romeo', and save the result."""
 
    input_file = pathlib.Path(FETCHED_DATA_DIR, "genesis.txt")

    output_file = pathlib.Path(PROCESSED_DIR, "text_God_word_count.txt")

    word_to_count: str = "God"

    word_count: int = count_word_occurrences(input_file, word_to_count)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the results to the output file
    with output_file.open('w') as file:
        file.write(f"Occurrences of '{word_to_count}': {word_count}\n")
    
    # Log the processing of the TEXT file
    logger.info(f"Processed text file: {input_file}, Word count saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting text processing...")
    process_text_file()
    logger.info("Text processing complete.")