import dataclasses
from functools import cached_property
from typing import List, Union
import pandas as pd
from libs.alum import Alum

from gsheet import google_sheet_helpers

# List of alumni to pull data for
ALUMNI_URLS: List = ["https://www.linkedin.com/in/sean-macbride/"]


@dataclasses.dataclass
class Alumni:
    alumni: List[Alum]

    @classmethod
    def from_urls_list(self, urls: List[str] = ALUMNI_URLS):
        alumni = [Alum.from_url(url) for url in urls]
        return Alumni(alumni=alumni)

    @classmethod
    def from_urls_csv(self, file_path: str):
        """Update spreadsheet from a csv of urls.

        Csv must be one-column, newline seperated, and headerless like:
            https://www.linkedin.com/abc/
            https://www.linkedin.com/def/
            https://www.linkedin.com/xyz/
        because I am lazy at the moment.
        """
        urls = list(pd.read_csv(file_path, header=None).stack().values)
        return Alumni.from_urls_list(urls=urls)

    @cached_property
    def alumni_dataset(self):
        alumni_dicts = [dataclasses.asdict(alum) for alum in self.alumni]
        return pd.DataFrame.from_records(alumni_dicts)

    def post_to_google_sheet(self):
        google_sheet_helpers.update_sheet(
            data=self.alumni_dataset, worksheet_name="Alumni"
        )
