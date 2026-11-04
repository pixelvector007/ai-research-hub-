import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "database"

AUTHORS_FILE = DATA_DIR / "authors.json"
USERS_FILE = DATA_DIR / "users.json"
RESEARCH_PAPERS_FILE = DATA_DIR / "research_papers.json"
COLLECTIONS_FILE = DATA_DIR / "collections.json"


def load_author_data():
    try:
        with open(AUTHORS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_author_data(data):
    with open(AUTHORS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_user_data():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_user_data(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_research_paper_data():
    try:
        with open(RESEARCH_PAPERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_research_paper_data(data):
    with open(RESEARCH_PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_collection_data():
    try:
        with open(COLLECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_collection_data(data):
    with open(COLLECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)