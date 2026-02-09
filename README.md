# Media renamer

Tools for renaming media files to add (year) and [tmdbid-###] tags. Useful for tidying/formatting files for use in Jellyfin server (or similar). Assumes files already named as per the movie.

Currently only for Movies.

Add your [TMDB API token and key](https://developer.themoviedb.org/docs/getting-started) to `.env.template` and rename to `.env`.

Run using [uv](https://docs.astral.sh/uv/):

```python
$ uv run utils.py --help # for help
$ uv run utils.py <folder with media files> --dry-run # scan media files and show changes but not make any changes (default)
$ uv run utils.py <folder with media files> --no-dry-run # scan media files and show changes but makes changes on file system 
$ uv run utils.py <folder with media files> --extension='mkv' # mkv file by default but can change to other file type 
$ uv run utils.py <folder with media files> --create-media-folder # creates a folder with same name as updated file name and moves file into it
$ uv run utils.py <folder with media files> --no-create-media-folder # (default) does not make new media folder and file stays in place
```