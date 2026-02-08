import os
import sys
import typing
import requests
import json
from pprint import pprint
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()
READ_ONLY_TOKEN = os.getenv("READ_ONLY_TOKEN")
API_KEY = os.getenv("API_KEY")

def get_file_names(folder: str, extension: str = "mkv") -> typing.List[tuple]:

    file_names = []
    for file in os.listdir(folder):
        if file.endswith(extension):
            file_names.append((file[: -(len(extension) + 1)], extension))
    return file_names


def tmdb_api_movie_search(query_str: str) -> dict:
    base_url = "https://api.themoviedb.org/"
    headers = {
        "Authorization": f"Bearer {READ_ONLY_TOKEN}",
        "accept": "application/json",
    }
    query = f"3/search/movie?query={quote(query_str)}&include_adult=false&language=en-US&page=1"
    response = requests.get(base_url + query, headers=headers)
    return response.json()

def make_new_namesList(file_names: typing.List[tuple]) -> typing.List[tuple[str, str]]:
    new_names: typing.List[tuple[str, str]] = []
    for name, ext in file_names:
        old_name: str = f"{name}.{ext}"
        tmdb_obj = tmdb_api_movie_search(name)
        if tmdb_obj["results"]:
            try:
                new_name: str = f"{tmdb_obj['results'][0]['title']} ({tmdb_obj['results'][0]['release_date'][:4]}) [tmdbid-{tmdb_obj['results'][0]['id']}].{ext}"
            except (KeyError, IndexError):
                new_name: str = f"{name}.{ext}" 
        new_names.append((old_name, new_name))     
    return new_names

if __name__ == "__main__":
    pprint(sys.argv)
    if len(sys.argv) < 2:
        print("Usage: python utils.py <folder_path> [extension]")
        sys.exit(1)

    folder_path = sys.argv[1]
    extension = sys.argv[2] if len(sys.argv) > 2 else "mkv"
    file_names = get_file_names(folder_path, extension)
    pprint(file_names)

    new_names = make_new_namesList(file_names)
    pprint(new_names)
