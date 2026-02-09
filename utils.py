import os
import typing

import requests
import typer

from dotenv import load_dotenv
from urllib.parse import quote

from rich import print
from rich.console import Console
from rich.table import Table
from rich.markup import escape
from rich.progress import track

load_dotenv()
READ_ONLY_TOKEN = os.getenv("READ_ONLY_TOKEN")
API_KEY = os.getenv("API_KEY")

console = Console(markup=False)
app = typer.Typer()

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


def make_new_names_list_movie(file_names: typing.List[tuple]) -> typing.List[tuple[str, str, str]]:
    new_names: typing.List[tuple[str, str, str]] = []
    print("")
    print("[green]Processing file names...")
    for name, ext in file_names:
        old_name: str = f"{name}"
        new_name: str = old_name
        tmdb_obj = tmdb_api_movie_search(name)
        if tmdb_obj["results"]:
            try:
                new_name: str = f"{tmdb_obj['results'][0]['title']} ({tmdb_obj['results'][0]['release_date'][:4]}) [tmdbid-{tmdb_obj['results'][0]['id']}]"
            except (KeyError, IndexError):
                pass
        print(escape(f"{old_name} -> {new_name}"), "*** Unchanged ***" if old_name == new_name else "")
        new_names.append((old_name, new_name, ext))
    print("[green]Done.")
    print("")
    return new_names


def file_ext(file_name: str, extension: str) -> str:
    return f"{file_name}.{extension}"


def rename_files(folder: str, new_names: typing.List[tuple[str, str, str]], create_media_folder: bool = False) -> None:
    for old_name, new_name, ext in track(new_names, description="[green]Renaming files..."):
        old_path = os.path.join(folder, file_ext(old_name, ext))
        if create_media_folder:
            new_path = os.path.join(folder, new_name)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            new_path = os.path.join(new_path, file_ext(new_name, ext))
        else:
            new_path = os.path.join(folder, file_ext(new_name, ext))
        os.rename(old_path, new_path)


@app.command()
def rename_movies(folder: str, extension: str = "mkv", dry_run: bool = True, create_media_folder: bool = False) -> None:
    file_names = get_file_names(folder, extension)
    new_names = make_new_names_list_movie(file_names)
    table = Table("Old", "New")

    if not dry_run:
        rename_files(folder, new_names, create_media_folder)
        print("[green]Done.")
        print("")

    for old, new, ext in new_names:
        if create_media_folder:
            table.add_row(f"{folder}/{file_ext(old, ext)}", f"{folder}/{new}/{file_ext(new, ext)}")
        else:
            table.add_row(f"{folder}/{file_ext(old, ext)}", f"{folder}/{file_ext(new, ext)}")
 
    console.print(table)

if __name__ == "__main__":
    app()
