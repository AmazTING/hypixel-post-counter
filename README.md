# Hypixel Thread Scraper & Stats Analyzer

This project scrapes a Hypixel forum thread, saves the posts to a CSV file, and then analyzes the collected data.

## Requirements
Ensure you have Python installed (version 3.x). Then, install the required dependencies using:

```sh
pip install -r requirements.txt
```

## Usage
To run the scripts, simply execute:

```sh
python main.py
```

## How It Works
1. **`scraper.py`** scrapes a given Hypixel thread and saves its posts to a CSV file inside the `threads/` folder.
2. **`stats.py`** processes the scraped data and generates statistics, saving them in the `thread_stats/` folder.
3. **`main.py`** serves as the entry point, running `scraper.py` first and then passing the results to `stats.py`.

## Input Format
When prompted, enter the full URL of the Hypixel thread. Example:

```
Enter the thread link: https://hypixel.net/threads/example-thread.123456/
```

## Output
- Scraped posts are saved in `threads/{thread_name}.csv`
- Statistics are stored in `thread_stats/{thread_name}_stats.csv`

## Notes
- The script automatically cleans the thread URL to extract a proper filename.
- Ensure `scraper.py` completes before `stats.py` starts (handled in `main.py`).

## Troubleshooting
- If an error occurs, check your internet connection and ensure the URL is correct.
- If Cloudflare blocks requests, consider using a VPN.
