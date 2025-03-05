# Hypixel Post Counter  

## Description  
Hypixel Post Counter is a Python tool that extracts and analyzes post data from Hypixel forum threads. It saves the data in a structured format and provides statistics on post counts.  

## Installation (from raw file)

1. Install Python (if not already installed).  
2. Install the required dependencies:  
   ```sh
   pip install -r requirements.txt
   ```  

## Usage  

1. Run the script:  
   ```sh
   python main.py
   ```  
2. Enter the thread link when prompted.  
3. The tool will process the thread and generate user statistics.  

## Output  

- A CSV file containing all posts will be saved in the `threads` folder.  
- Statistics will be saved in the `thread_stats` folder.  
