# Flight Monitor

Simple python dash app to monitor flight prices. The prices will be updated every 30 minutes.

Install python dependencies with:
```powershell
pip install -r requirements.txt
```

## Usage

Firstly create a `.json` file, that contains the flights you want to monitor, such as:
```json
[
	{
		"departure": "VIE",
		"arrival": "TGD",
		"date": "2025-07-18",
		"agency": "wizzair"
	},
]
```
The departure and arrival strings are airport codes, date should be in format "YYYY-MM-DD".

**Currently supported flight agencies**

 - [x] Wizzair
 - [x] Ryanair

Then run the app with:
```
python app.py [-h] [--adults ADULTS] [--flights_file FLIGHTS_FILE] [--data_file DATA_FILE]

options:
  -h, --help            show this help message and exit
  --adults              number of adult passangers
  --flights_file        json file: list of flight dicts [\{"departure": "DDD", "arrival": "AAA", "date": "YYYY-MM-DD", "agency": "<agency>"\}, ...]
  --data_file           csv filepath to save and load saved data if already exists
```

The app launches a server on localhost at port 8050, you can access it [via web browser](http://127.0.0.1:8050/).
