"""
Process a CSV file on 2019 NCAA Women's Volleyball to analyze the 'Home Team' column and save statistics.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import csv
import statistics
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

# TODO: Add or replace this with a function that reads and processes your CSV file

def calculate_home_court_advantage(file_path: pathlib.Path) -> dict[str, float]:
    """Calculate % of matches won by home teams."""
    match_results = {}

    with file_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            match_id = row["match_id"]
            if match_id not in match_results:
                # Only need one row per match to know final result
                home_sets = int(row["home_team_set_score"])
                away_sets = int(row["visiting_team_set_score"])
                match_results[match_id] = (home_sets, away_sets)

    total_matches = len(match_results)
    home_wins = sum(1 for hs, vs in match_results.values() if hs > vs)

    return {
        "total_matches": total_matches,
        "home_wins": home_wins,
        "home_win_pct": (home_wins / total_matches * 100) if total_matches > 0 else 0,
    }

def process_csv_file():
    """Read a CSV file, analyze home court advantage, and save the results."""
    
    input_file = pathlib.Path(FETCHED_DATA_DIR, "2019_NCAA_Womens_Volleyball.csv")
    
    output_file = pathlib.Path(PROCESSED_DIR, "home_court_advantage.txt")
    
    # TODO: Call your new function to process YOUR CSV file
    # TODO: Create a new local variable to store the result of the function call
    
    stats = calculate_home_court_advantage(input_file)

    # Create the output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Open the output file in write mode and write the results
    with output_file.open('w') as file:

        # TODO: Update the output to describe your results
        file.write("Home Court Advantage Analysis\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total matches: {stats['total_matches']}\n")
        file.write(f"Home team wins: {stats['home_wins']}\n")
        file.write(f"Home win %: {stats['home_win_pct']:.2f}%\n")
    
    # Log the processing of the CSV file
    logger.info(f"Processed CSV file: {input_file}, Results saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting CSV processing...")
    process_csv_file()
    logger.info("CSV processing complete.")