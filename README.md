# Python-client
A python client to connect to Zodiac for data services.

Install Python dependencies with
` pip install -r requirements.txt`

## Data Upload

Upload files via:

`zodiac.py [-h] -f FILEPATH -d DESCRIPTION -u USERNAME -p PASSWORD`

Example:

 `python zodiac.py -f test_file.csv -d "transaction log file" -u user@company.com -p my_password`

See example usage from the command line via:

   `python zodiac.py`


## Data Download

In a python application import 
`api.Zodiac` 

Instantiate it with your credentials (username, password).  On the instance call `list_datasets` to see your available files, and then get the download link by calling `get_download_url` providing it with the filename.  


