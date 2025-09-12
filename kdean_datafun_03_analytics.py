"""
Run 8 scripts in order with logging, fixed CWD, and post-run dir checks.
"""

import pathlib
import sys
import time
import subprocess
from typing import List, Tuple

from utils_logger import logger

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

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

DELAY_BETWEEN_SCRIPTS = 10
STOP_ON_ERROR = False

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent

# IMPORTANT: Set this to the directory where your scripts expect
# relative folders like "karlidean_data" and "karlidean_processed".
# If your scripts & data dirs sit next to this runner, leave as PROJECT_ROOT.
# If they live under "src", use PROJECT_ROOT / "src".
WORKING_DIR = PROJECT_ROOT  # or: PROJECT_ROOT / "src"

# If your child scripts accept CLI flags like --overwrite, you can pass them here.
EXTRA_ARGS = {
    # "karlidean_get_csv.py": ["--overwrite"],
}

# For convenience checks after each script
FETCHED_DATA_DIR = WORKING_DIR / "karlidean_data"
PROCESSED_DATA_DIR = WORKING_DIR / "karlidean_processed"

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def list_dir_safe(path: pathlib.Path, label: str) -> None:
    """Log a short listing of a directory if it exists."""
    if not path.exists():
        logger.info(f"[post-check] {label} does not exist: {path}")
        return
    try:
        items = sorted([p.name for p in path.iterdir()])
        preview = ", ".join(items[:8])
        more = "" if len(items) <= 8 else f" (+{len(items)-8} more)"
        logger.info(f"[post-check] {label} => {path} :: {preview}{more}")
    except Exception as ex:
        logger.warning(f"[post-check] Could not list {label} at {path}: {ex}")

def resolve_scripts() -> List[pathlib.Path]:
    """Resolve script paths relative to WORKING_DIR, then PROJECT_ROOT."""
    resolved, missing = [], []
    for name in SCRIPTS_TO_RUN:
        p1 = WORKING_DIR / name
        p2 = PROJECT_ROOT / name
        if p1.exists():
            resolved.append(p1)
        elif p2.exists():
            resolved.append(p2)
        else:
            missing.append(name)
    if missing:
        logger.error(f"The following scripts were not found: {', '.join(missing)}")
    return resolved

def run_script(script_path: pathlib.Path) -> int:
    """Run a Python script and stream its output to the logger."""
    logger.info(f"Initializing Script Run for {script_path.name}")
    logger.info(f"Using CWD: {WORKING_DIR}")

    cmd = [sys.executable, str(script_path)]
    if script_path.name in EXTRA_ARGS:
        cmd.extend(EXTRA_ARGS[script_path.name])

    try:
        completed = subprocess.run(
            cmd,
            cwd=str(WORKING_DIR),
            text=True,
            capture_output=True,
        )
    except FileNotFoundError as ex:
        logger.error(f"Python or script not found when running {script_path.name}: {ex}")
        return 127
    except OSError as ex:
        logger.error(f"OS error when running {script_path.name}: {ex}")
        return 126

    if completed.stdout:
        for line in completed.stdout.splitlines():
            logger.info(f"[{script_path.name}][stdout] {line}")
    if completed.stderr:
        for line in completed.stderr.splitlines():
            logger.warning(f"[{script_path.name}][stderr] {line}")

    rc = completed.returncode
    if rc == 0:
        logger.info(f"Completed {script_path.name} (exit code 0).")
    else:
        logger.error(f"{script_path.name} failed (exit code {rc}).")
    return rc

# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main() -> int:
    logger.info("Initializing Combined Runner for all scripts...")
    logger.info(f"Project root: {PROJECT_ROOT}")
    logger.info(f"Run directory (CWD for children): {WORKING_DIR}")

    scripts = resolve_scripts()
    if not scripts:
        return 1

    failures: List[Tuple[str, int]] = []

    for idx, script_path in enumerate(scripts, start=1):
        logger.info(f"({idx}/{len(scripts)}) {script_path.name}")
        rc = run_script(script_path)

        # Post-run sanity checks: did anything land where we expect?
        list_dir_safe(FETCHED_DATA_DIR, "karlidean_data")
        list_dir_safe(PROCESSED_DATA_DIR, "karlidean_processed")

        if rc != 0:
            failures.append((script_path.name, rc))
            if STOP_ON_ERROR:
                logger.error("Stopping due to failure and STOP_ON_ERROR=True.")
                return rc

        if idx < len(scripts):
            logger.info(f"Waiting {DELAY_BETWEEN_SCRIPTS} seconds before next script...")
            time.sleep(DELAY_BETWEEN_SCRIPTS)

    if failures:
        logger.warning("Completed with failures:")
        for name, rc in failures:
            logger.warning(f" - {name} (exit code {rc})")
        return 2

    logger.info("All scripts ran successfully.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
