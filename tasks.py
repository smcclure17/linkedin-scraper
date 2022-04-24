"""Invoke command line tasks

To execute run: inv [command] --argname "argvalue"
e.g.: inv update-from-csv-urls --file "data/alumni_urls.csv"
"""

from libs.alumni import Alumni
from invoke import task


@task(
    help={
        "file": "path to CSV/text file containing LinkedIn URLS. Must be one-column, headerless, newline-separated."
    },
    optional=["file"],
)
def update_from_csv_urls(ctx, file="data/alumni_urls.csv"):
    """Update google sheet with info from profiles in file.

    LinkedIn credentials must be set in system environment (see README) to execute.
    TODO: Add an option to pass in LinkedIn credentials here?
    """
    alums = Alumni.from_urls_csv(file_path=file)
    alums.post_to_google_sheet()
