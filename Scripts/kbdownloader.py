import csv
import os
import time
import argparse
import re
from datetime import datetime
from urllib.parse import urlparse
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore

start_time = datetime.now()
timestamp_str = start_time.strftime('%Y-%m-%d_%H-%M-%S')

## ------------------------------------------ UTILITIES ------------------------------------------ ##

# I need to be careful with file names because Copilot requires the name be less than 100 characters, 
# but while I'm there, might as well check for special characters that might crash on Windows or macOS, too.
def sanitize_filename(filename, max_length=100):
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    filename = filename.strip()
    name, ext = os.path.splitext(filename)
    allowed_length = max_length - len(ext)
    if len(name) > allowed_length:
        name = name[:allowed_length]
    return name + ext

# This is so we can a header row and any non-url garbage data
def is_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        print(f"{s} is not a url, skipping...")
        return False

def is_null_or_whitespace(s):
    return s is None or s.strip() == ''


## ------------------------------------------ WORKERS ------------------------------------------ ##

def save_kb(url, output_folder_name, driver, concatenate):
    try:
        print("Getting page...")

        # Loads the web page into the browser
        driver.get(url)

        print("Waiting for content load...")
        
        # Important Discovery
        # The KB content is not immediately visible, it gets rendered long after the page loads. 
        # I've found the last DOM element in the content area is the "Last Updated" div, 
        # so this waits until that element has been rendered before we scrape the content.
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-aura-class="uiOutputDateTime"]'))
        )

        print("Finding <article.content> element...")

        content_article = driver.find_element(By.CSS_SELECTOR, "article.content[data-aura-rendered-by]")

        elapsed = datetime.now() - start_time
        elapsed_str = str(elapsed).split('.')[0] # HH:MM:SS
        
        if content_article:
            print("Separating article text from HTML/CSS...")
            content = content_article.text
            
            if concatenate:
                output_path = os.path.join(os.getcwd(), output_folder_name, "all_kb_articles.txt")  

                with open(output_path, 'a', encoding='utf-8') as file:
                    file.write(f"KB: {url}\n")
                    file.write("---------------------------------------------------------------------------\n")
                    file.write(content)
                    file.write("\n---------------------------------------------------------------------------\n\n\n")

                print(f"Appended content from {url} | Time Elapsed: {elapsed_str}")
            else:
                parsed_url = urlparse(url)
                raw_filename = parsed_url.path.replace('/', '_') + '.txt'
                filename = sanitize_filename(raw_filename)
                filepath = os.path.join(os.getcwd(), output_folder_name, filename)

                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)

                print(f"Saved {url} as {filename} | Time Elapsed: {elapsed_str}")
        else:
            print(f"Skipped: Could not find <article.content> tag in {url}  | Time Elapsed: {elapsed_str}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def start(csv_file, output_folder, concatenate):
    if is_null_or_whitespace(csv_file):
        print("No CSV file provided, please provide a csv file path in the first or '--csv_file' argument. Exiting...")
        return

    # Add a timestamp to the folder and ensures the directory exists
    start_time.strftime('%Y-%m-%d_%H-%M-%S')
    dated_output_folder = f"{output_folder}_{timestamp_str}"
    if not os.path.exists(dated_output_folder):
        os.makedirs(dated_output_folder)

    # Create a headless web browser so we can load the webpages in memory
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Open the CSV file and iterate over the rows
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[0]
            # I skip any header row, or non URL entries
            if is_url(url):
                save_kb(url, dated_output_folder, driver, concatenate)
                time.sleep(1)
    driver.quit()

## ------------------------------------------ ENTRY POINT ------------------------------------------ ##
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download KB articles as a single, or separate, .txt files.')
    parser.add_argument('--csv_file', type=str, help='Path to the input CSV file containing URLs.')
    parser.add_argument('--output_folder_name', type=str, nargs='?', default='download', help='Output folder name (name only, not a full path).')
    parser.add_argument('--concatenate', type=bool, default=True, nargs='?', help='Save ')
    args = parser.parse_args()

start(args.csv_file, args.output_folder_name, args.concatenate)
