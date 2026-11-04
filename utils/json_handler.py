import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "database"

AUTHORS_FILE = DATA_DIR / "authors.json"
USERS_FILE = DATA_DIR / "users.json"
RESEARCH_PAPERS_FILE = DATA_DIR / "research_papers.json"
COLLECTIONS_FILE = DATA_DIR / "collections.json"


def load_data(file_path: Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(file_path: Path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
