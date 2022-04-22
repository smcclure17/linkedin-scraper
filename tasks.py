"""Invoke command line tasks

To execute run: inv [command] --argname "argvalue"
e.g.: inv update-from-csv-urls --file "data/alumni_urls.csv"
"""

from libs.alumni import Alumni
from invoke import task


@task(
    help={
        "file": "path to CSV containing LinkedIn URLS. Must be one-column, headerless, newline-separated."
    },
    optional=["file"],
)
def update_from_csv_urls(ctx, file="data/alumni_urls.csv"):
    alums = Alumni.from_urls_csv(file_path=file)
    alums.post_to_google_sheet()
