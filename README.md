# Python-client
A python client to connect to Zodiac for data services.

## Installation

Install Python dependencies with
` pip install -r requirements.txt`


For all programmatic uploads if you have a private cloud please use
`--api` to provide your API end point, usually matching the pattern `https://privateaccount.zodiacmetrics.com/api`


## Pilot Data Upload

Upload files via:

`zodiac.py [-h] -f FILEPATH -d DESCRIPTION -u USERNAME -p PASSWORD`

Example:

 `python zodiac.py -f test_file.csv -d "transaction log file" -u user@company.com -p my_password`

See example usage from the command line via:

   `python zodiac.py`


## Data Upload for Job Run

For clients using continuous programmatic upload, please use this option. Before beginning, talk to your client success representative to set up data schemas.

Upload files via:
 `zodiac-job.py -m HASH_PROVIDED_BY_ZODIAC -u USERNAME -p PASSWORD -t TRANSACTION_LOG_FILE -a ATTRIBUTES_FILE`

See example usage from the command line via:

`python zodiac-job.py --help`

**Notes:**

1. Transaction logs are considered append-only and the job processor will keep only new transactions since the last job run.

1. Attribute files must be _complete for the entire customer base_. Customers missing from the uploaded attributes files that appear in the full transaction log (including previous uploads) will be assumed to have missing values for all attributes.


1. Transaction log and attribute headers are expected to conform to those provided in the initial client onboarding. If you'd like to have the schemas updated, please contact your client success representative.

## Upload Emails

For clients using emails, please use this option.

Upload files via:
 `zodiac-emails.py -u USERNAME -p PASSWORD -e EMAIL_FILE -c COMPANY_MASK`

See example usage from the command line via:

`python zodiac-email.py --help`


##Download Client
To get a copy of whatever the latest model out put is use this option.

`zodiac-output `

## Output Download

1. All transaction log data must be complete. Rows with missing data are excluded.

In a python application import
`python zodiac-output.py -u USERNAME -p PASSWORD -c COMPANY_MASK`

**Notes:**
This only downloads the latest model output for a company.  If you have multiple models
you will want to use the more advanced facilities below.

See example usages from the command line via:
`python zodiac-output.py --help`


## Download Multiple Files

Instantiate the Zodiac class with your credentials (username, password).  On the instance call `list_datasets` to see your available files.

To retrieve a file, get the download link by calling `get_download_url` providing the method with the filename.


```
import requests
import api

conn = api.Zodiac('user@company.com', 'my_password')
print conn.list_datasets() # see a list of available files for download
url = conn.get_download_url('results.csv')

# This is a way to download the file from the url using the requests module
# The file can be downloaded by any other means such as curl, wget, etc.

def download_file(url, local_filename):
    '''See http://docs.python-requests.org/en/latest/user/advanced/#body-content-workflow '''
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

download_file(url, 'local_result.csv')
```
