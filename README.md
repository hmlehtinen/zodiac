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
