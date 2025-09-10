"""
Process a JSON file to count stars by spectral group (O, B, A, F, G, K, M)
and save the result as a text file.

Input format: a JSON array of star records (dicts) containing "SpectralCls".
"""

#####################################
# Import Modules
#####################################

# Python Standard Library
import json
import pathlib
import sys

# Ensure project root is in sys.path for local imports
sys.path.append(str(pathlib.Path(__file__).resolve().parent))

# Local modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

# Folders (change if needed)
FETCHED_DATA_DIR: str = "karlidean_data"
PROCESSED_DIR: str = "karlidean_processed"

# Filenames (change if needed)
INPUT_FILENAME = "stars.json"
OUTPUT_FILENAME = "stars_by_spectral_group.txt"

# Canonical spectral order
SPECTRAL_ORDER = "OBAFGKM"
SPECTRAL_INDEX = {c: i for i, c in enumerate(SPECTRAL_ORDER)}

#####################################
# Define Functions
#####################################

def spectral_group(spectral_cls: str) -> str:
    """
    Extract the leading spectral class letter (O/B/A/F/G/K/M).
    Returns 'Unknown' if missing or nonstandard.
    """
    if not spectral_cls:
        return "Unknown"
    s = str(spectral_cls).strip().upper()
    if not s:
        return "Unknown"
    return s[0] if s[0] in SPECTRAL_INDEX else "Unknown"


def count_stars_by_spectral_group(file_path: pathlib.Path) -> dict:
    """
    Count stars by spectral group from a JSON file.

    Accepts:
      - a list of star dicts (preferred; matches your sample), or
      - a dict whose first list-like value contains the star records.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Error reading or parsing JSON: {e}")
        return {}

    # Normalize to a list of records
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        # Try to find a list within the dict (fallback)
        candidates = [v for v in data.values() if isinstance(v, list)]
        records = candidates[0] if candidates else []
    else:
        records = []

    counts = {c: 0 for c in SPECTRAL_ORDER}
    counts["Unknown"] = 0

    for rec in records:
        if not isinstance(rec, dict):
            continue
        group = spectral_group(rec.get("SpectralCls"))
        counts[group] = counts.get(group, 0) + 1

    return counts


def process_json_file():
    """Read the star JSON, count by spectral group, and save a TXT summary."""
    input_file: pathlib.Path = pathlib.Path(FETCHED_DATA_DIR, INPUT_FILENAME)
    output_file: pathlib.Path = pathlib.Path(PROCESSED_DIR, OUTPUT_FILENAME)

    counts = count_stars_by_spectral_group(input_file)

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write ordered text report
    with output_file.open('w', encoding='utf-8') as file:
        file.write("Stars by Spectral Group\n")
        file.write("=======================\n\n")
        file.write(f"Input file: {input_file}\n")
        total = sum(counts.values())
        file.write(f"Total stars counted: {total}\n\n")
        file.write("Counts:\n")
        for c in SPECTRAL_ORDER:
            file.write(f"  {c}: {counts.get(c, 0)}\n")
        file.write(f"  Unknown: {counts.get('Unknown', 0)}\n")

    logger.info(f"Processed JSON file: {input_file}, results saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting star JSON processing...")
    process_json_file()
    logger.info("Processing complete.")
