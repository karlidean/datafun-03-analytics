from pathlib import Path
import csv
import json
import requests
from openpyxl import Workbook
from utils_logger import logger

def fetch_todos(url: str) -> list[dict]:
    logger.info(f"Fetching {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return resp.json()

def process_todos(data: list[dict]) -> list[tuple]:
    logger.info("Processing data")
    return [
        (d.get("userId"), d.get("id"), (d.get("title") or "").strip(), bool(d.get("completed")))
        for d in data
    ]

def write_csv(rows: list[tuple], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["userId", "id", "title", "completed"])
        w.writerows(rows)

def write_excel(rows: list[tuple], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "todos"
    ws.append(["userId", "id", "title", "completed"])
    for r in rows:
        ws.append(list(r))
    wb.save(path)

def write_json(rows: list[tuple], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(
            [{"userId": r[0], "id": r[1], "title": r[2], "completed": r[3]} for r in rows],
            f,
            indent=2,
        )

def write_txt(rows: list[tuple], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(f"userId={r[0]}, id={r[1]}, title={r[2]}, completed={r[3]}\n")

def main() -> None:
    logger.info("Starting Project 3")
    url = "https://jsonplaceholder.typicode.com/todos"
    processed = process_todos(fetch_todos(url))

    data_dir = Path("data")  # <- use this name consistently
    write_csv(processed,  data_dir / "todos.csv")
    write_excel(processed, data_dir / "todos.xlsx")
    write_json(processed,  data_dir / "todos.json")
    write_txt(processed,   data_dir / "todos.txt")

    logger.info(f"Wrote {len(processed)} rows to data/")
    logger.info("Done.")

if __name__ == "__main__":
    main()