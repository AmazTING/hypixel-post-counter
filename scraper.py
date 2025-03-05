import cfscrape
from bs4 import BeautifulSoup
import csv
import eta
import unicodedata
import re
import argparse
import sys
import os

def slugify(value, allow_unicode=False):
    """Converts a string into a URL-friendly slug format."""
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def clean_thread_url(thread_url):
    """Removes page numbers and post references from the thread URL."""
    thread_url = thread_url.rstrip('/')  # Remove trailing slash
    thread_url = re.sub(r'/page-\d+', '', thread_url)  # Remove page-XX
    thread_url = re.sub(r'#post-\d+', '', thread_url)  # Remove #post-XXXXXX
    return thread_url

def generate_thread_name(thread_url):
    """Removes page numbers, post references, and the URL prefix from the thread URL."""
    # Remove the prefix
    thread_url = re.sub(r'https?://hypixel\.net/threads/', '', thread_url)
    thread_url = thread_url.rstrip('/')  # Remove trailing slash
    thread_url = re.sub(r'/page-\d+', '', thread_url)  # Remove page-XX
    thread_url = re.sub(r'#post-\d+', '', thread_url)  # Remove #post-XXXXXX
    thread_url = re.sub(r'\.\w+', '', thread_url)  # Remove the dot and following characters
    return thread_url

def scrape_thread(thread_url):
    """Scrapes a Hypixel forum thread and saves the posts to a CSV file inside the 'threads' folder."""

    thread_url = clean_thread_url(thread_url)  # Clean the URL before scraping
    scraper = cfscrape.create_scraper()

    try:
        response = scraper.get(thread_url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching thread: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    # Get total page count
    page_nav = soup.findAll("li", {"class": "pageNav-page"})
    page_count = int(page_nav[-1].text) if page_nav else 1

    print(f"Thread has {page_count} pages.")

    # Get thread name and set up file path
    thread_name = generate_thread_name(thread_url)

    # Ensure 'threads' folder exists
    os.makedirs("threads", exist_ok=True)

    csv_filename = os.path.join("threads", f"{thread_name}.csv")

    with open(csv_filename, "w", newline="", encoding="UTF-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(["Author", "Post", "Timestamp"])

    eta_tracker = eta.ETA(page_count)

    for i in range(1, page_count + 1):
        try:
            page_response = scraper.get(f"{thread_url}/page-{i}")
            page_response.raise_for_status()
        except Exception as e:
            print(f"Error fetching page {i}: {e}")
            continue

        page_soup = BeautifulSoup(page_response.content, "html.parser")

        posts_data = []

        for post in page_soup.findAll("article", {"class": "message message--post js-post js-inlineModContainer"}):
            author = post["data-author"]
            timestamp = post.find("time", {"class": "u-dt"})["data-timestamp"]

            bbwrapper = post.find("div", {"class": "bbWrapper"})

            # Remove blockquotes
            for blockquote in bbwrapper.findAll("blockquote"):
                blockquote.decompose()

            post_text = "\n".join(line.strip() for line in bbwrapper.text.splitlines())

            posts_data.append([author, post_text, timestamp])

        # Write posts to CSV
        with open(csv_filename, "a", newline="", encoding="UTF-8") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            csvwriter.writerows(posts_data)

        eta_tracker.print_status(i)

    eta_tracker.done()
    print(f"Scraping complete. Data saved to {csv_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape a Hypixel forum thread and save it as a CSV file.")
    parser.add_argument("thread_url", help="The full URL of the Hypixel forum thread")
    args = parser.parse_args()

    print(scrape_thread(args.thread_url))
