from utils.json_handler import (
    AUTHORS_FILE,
    COLLECTIONS_FILE,
    RESEARCH_PAPERS_FILE,
    USERS_FILE,
    load_data,
)


def get_author_data():
    return load_data(AUTHORS_FILE)


def get_collection_data():
    return load_data(COLLECTIONS_FILE)


def get_research_paper_data():
    return load_data(RESEARCH_PAPERS_FILE)


def get_user_data():
    return load_data(USERS_FILE)
