# Python-client
A python client to connect to Zodiac for data services.

## Installation

Install Python dependencies with
` pip install -r requirements.txt`

## Pilot Data Upload

Upload files via:

`zodiac.py [-h] -f FILEPATH -d DESCRIPTION -u USERNAME -p PASSWORD`

Example:

 `python zodiac.py -f test_file.csv -d "transaction log file" -u user@company.com -p my_password`

See example usage from the command line via:

   `python zodiac.py`


## Data Upload for Job Run

For clients using continuous programmatic upload, please use this option.

Upload files via:
 `zodiac-job.py -m HASH_PROVIDED_BY_ZODIAC -u USERNAME -p PASSWORD -t TRANSACTION_LOG_FILE -a ATTRIBUTES_FILE`

See example usage from the command line via:

`python zodiac-job.py --help`

**Notes:**

1. Transaction logs are considered append-only and the job processor will keep only new transactions since the last job run.

2. Attribute files must be _complete for the entire customer base_. Customers missing from the uploaded attributes files that appear in the full transaction log (including previous uploads) will be assumed to have missing values for all attributes.

## Data Download

In a python application import
`api.Zodiac`

Instantiate the Zodiac class with your credentials (username, password).  On the instance call `list_datasets` to see your available files.

To retrieve a file, get the download link by calling `get_download_url` providing the method with the filename.

### Download example

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
