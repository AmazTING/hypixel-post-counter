import subprocess
import sys
import re

import re

def clean_thread_url(thread_url):
    """Removes page numbers, post references, and the URL prefix from the thread URL."""
    # Remove the prefix
    thread_url = re.sub(r'https?://hypixel\.net/threads/', '', thread_url)
    thread_url = thread_url.rstrip('/')  # Remove trailing slash
    thread_url = re.sub(r'/page-\d+', '', thread_url)  # Remove page-XX
    thread_url = re.sub(r'#post-\d+', '', thread_url)  # Remove #post-XXXXXX
    thread_url = re.sub(r'\.\w+', '', thread_url)  # Remove the dot and following characters
    return thread_url



def run_scripts(thread_url):
    """Runs scraper.py and stats.py in sequence for a given thread, showing live output including ETA progress."""

    def run_process(command):
        """Runs a subprocess and ensures its output is displayed live, including real-time updates."""
        process = subprocess.Popen(
            command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            bufsize=1
        )

        process.wait()


    # Run scraper.py and capture thread name from its output
    print("\n>>> Running scraper.py...\n")
    run_process(["python", "scraper.py", thread_url])

    thread_name = clean_thread_url(thread_url)

    # Run stats.py using the extracted thread name
    print("\n>>> Running stats.py...\n")
    run_process(["python", "stats.py", thread_name])

if __name__ == "__main__":
    thread_url = input("Enter the thread link: ").strip()
    run_scripts(thread_url)
