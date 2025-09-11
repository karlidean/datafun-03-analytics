"""
This script is a combination of the "get" files and the
"process" files that are within this repo.

It should run all 8 scripts in order with a 10-second delay
between each one.

#   - Update the script filenames in SCRIPTS_TO_RUN if needed.
#   - Adjust DELAY_BETWEEN_SCRIPTS to your preferred wait time.
#   - Choose how to handle failures (STOP_ON_ERROR).
#   - (Optional) Set WORKING_DIR if scripts must run from a subfolder.
"""

##########
# Imports (Standard Library + local utils)
##########
import pathlib
import sys
import time
import subprocess

# Import your project logger
from utils_logger import logger

##########
# Configuration (Edit these TODOs)
##########

SCRIPTS_TO_RUN = [
    "karlidean_get_csv.py",
    "karlidean_get_excel.py",
    "karlidean_get_json.py",
    "karlidean_get_text.py",
    "karlidean_process_csv.py",
    "karlidean_process_excel.py",
    "karlidean_process_json.py",
    "karlidean_process_text.py",
]

# This is the delay in seconds between each script run.
DELAY_BETWEEN_SCRIPTS = 10

# If True, stop immediately when a script fails (non-zero exit code).
STOP_ON_ERROR = False

# (Optional): If your 8 scripts must be run from a specific folder
#       (for example, they assume relative paths like "data/" exist),
#       set WORKING_DIR to that folder. Otherwise leave as None.
# With None, the Scripts will be running from this same folder (in this case that's ok)
WORKING_DIR = None  # or pathlib.Path("path/to/folder")

##########
# Derived paths (usually no changes needed)
##########

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent
RUN_DIR = pathlib.Path(WORKING_DIR).resolve() if WORKING_DIR else PROJECT_ROOT

##########
# Helpers
##########

def run_script(script_path: pathlib.Path) -> int:
    """
    Run a Python script via the current interpreter and return its exit code.
    """
    # New log line at the very beginning of each script run
    logger.info(f"Initializing Script Run for {script_path.name}")

    logger.info(f"Running {script_path.name} ...")
    completed = subprocess.run([sys.executable, str(script_path)], cwd=str(RUN_DIR))
    rc = completed.returncode
    if rc == 0:
        logger.info(f"Completed {script_path.name} (exit code 0).")
    else:
        logger.error(f"{script_path.name} failed (exit code {rc}).")
    return rc

##########
# Main
##########

def main() -> int:
    logger.info("Initializing Combined Runner for all scripts...")

    # Validate scripts exist before starting
    missing = []
    resolved_scripts = []
    for name in SCRIPTS_TO_RUN:
        candidate = (RUN_DIR / name) if (RUN_DIR / name).exists() else (PROJECT_ROOT / name)
        if not candidate.exists():
            missing.append(name)
        else:
            resolved_scripts.append(candidate)

    if missing:
        logger.error("The following scripts were not found: %s", ", ".join(missing))
        return 1

    failures = []

    for idx, script_path in enumerate(resolved_scripts, start=1):
        logger.info("(%d/%d) %s", idx, len(resolved_scripts), script_path.name)
        rc = run_script(script_path)
        if rc != 0:
            failures.append((script_path.name, rc))
            if STOP_ON_ERROR:
                logger.error("Stopping due to failure and STOP_ON_ERROR=True.")
                return rc

        if idx < len(resolved_scripts):
            logger.info("Waiting %d seconds before next script...", DELAY_BETWEEN_SCRIPTS)
            time.sleep(DELAY_BETWEEN_SCRIPTS)

    if failures:
        logger.warning("Completed with failures:")
        for name, rc in failures:
            logger.warning(" - %s (exit code %d)", name, rc)
        return 2

    logger.info("All scripts ran successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
