# Rugby Alumni LinkedIn Scraper

Simple, pseudo-generic tooling for extracting user Info from LinkedIn profiles, and posting that data to Google Sheets. 


## Setup

### Create a Conda env. and install dependencies

- If necessary, download and install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html), a Python environment handler. 

- Create an environment (I'll call mine `rugby-alumni` for this example),

    ```bash
    conda create -n rugby-alumni python=3.9
    ```

- Say yes to anything it asks you, then activate your environment,

    ```bash
    conda activate rugby-alumni
    ```

- Run the makefile to install the necessary dependencies, 

    ```bash
    make setup-dev
    ```

### Setup gsheet service account credentials 

- Ask Sean (McClure) for a copy of the ghseet service account key
- Folow the step 7 in the [Gsheet package documentation]() to put the account key in the correct location such that the library can access it: 

    > Move the downloaded file to `~/.config/gspread/service_account.json`. Windows users should put this file to `%APPDATA%\gspread\service_account.json`.

- Test that everything was successful by running the following in an interactive python window:
    ```python
    from gsheet.google_sheet_helpers import init_service_account
    init_service_account()
    ```
    
    NOTE: I really don't like this method, and we should find a way to use a standard env variable or something.

## Setup LinkedIn account credentials

This repo relies on LinkedIn credentials (email and password) stored in environment variables to make requests against the LinkedIn API/server. I have created an empty/new account specifically for this so that we don't use our real accounts, reach out to me (Sean McClure) for the credentials.

### Setting environment variables.

To set the environment variables such that the code can access them, on Mac or Linux, run: 

```bash
export LINKEDIN_USER="{email address here}"
export LINKEDIN_PASS="{password here}"
```

These variables are then accessed by the Alum class.

## Usage

The main usage at the moment is to update a [google sheet](https://docs.google.com/spreadsheets/d/1L4G0mM_iti_H5burWq22g4v4jMZW-4LhX8BvnH5o_WI/edit#gid=0) with personal data from LinkedIn profiles. 
We specify the profiles we want to scrape with URLS in a csv (by default `data/alumni_urls.csv`). 

To run, we can use command line tools from the `invoke` package. 

To update the google sheet with data from the urls in `data/alumni_urls.csv`, run:
```
inv update-from-csv-urls
```

To update from any other csv, run:
```
inv update-from-csv-urls --file "path/to/file.csv"
```

At the moment, there is near-zero error handling, so things may go very wrong.


