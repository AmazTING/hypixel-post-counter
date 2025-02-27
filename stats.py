import csv
import re
import os
import sys

# Ensure output directory exists
os.makedirs("thread_stats", exist_ok=True)

# Gather statistics from the CSV file
name = sys.argv[1]

# Paths for input and output files
input_file = os.path.join("threads", f"{name}.csv")
stats_csv_file = os.path.join("thread_stats", f"{name}_stats.csv")

authors = []
messages = []
timestamps = []

# Open CSV file and read data
try:
    with open(input_file, "r", newline="", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)  # Skip header if it exists
        for row in reader:
            authors.append(row[0])
            if re.search('[a-zA-Z]', row[1]):
                messages.append(row[1])
            # timestamps.append(int(row[2]))  # Uncomment if needed
except FileNotFoundError:
    print(f"Error: File '{input_file}' not found.")
    exit(1)

# Count the frequency of each author
authorCount = {}
for author in authors:
    authorCount[author] = authorCount.get(author, 0) + 1

# Read previous stats if they exist
oldstats = {}
try:
    with open(stats_csv_file, "r", encoding='UTF-8') as csvfile:
        oldstats = {row[0]: int(row[1]) for row in csv.reader(csvfile, delimiter=",")}
except FileNotFoundError:
    pass

# Calculate differences from the last run
authorCount = sorted(authorCount.items(), key=lambda x: x[1], reverse=True)
diff = [count - oldstats.get(author, 0) for author, count in authorCount]

# Write results to stats files
with open(stats_csv_file, "w", encoding='UTF-8') as f:
    for author, count in authorCount:  # Write all to CSV
        f.write(f"{author},{count}\n")

print(f"Statistics saved to '{stats_csv_file}'.")

