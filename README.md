# web_scraper_1
Web scraper for e-shop

## Installation
1. Copy params file

`cp params.json.example params.json`

2. Edit params file
3. Edit crontab

`crontab -e`

4. Append crontab file

`/10 * * * * /usr/bin/python /path/to/project/main.py`

5. Execute

`python3 main.py`
