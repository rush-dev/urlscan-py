# urlscan-py
python script for submitting URL's to the urlscan.io API, retrieve the results, and post to output.

# Requirements (Setup)

- Python 3.6+
- Requests
- API key from urlscan.io (free on account creation, simply change the api_key variable to your key before running)
```
pip install Requests
```
- Argparse
```
pip install argparse
```
- Time
```
pip install time
```
- tqdm
```
pip install tqdm
```

## Usage
```
python urlscan.py -u google.com
python urlscan.py --url google.com
```

# Troubleshooting
- If you are receiving errors, please look at the Issues queue and see if there is already an issue open.

- If you have a unique issue, please create a new Issue, and include the output of your terminal.
