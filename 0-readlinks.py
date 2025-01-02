import requests
from bs4 import BeautifulSoup
import os
import re

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

def extract_links_and_filter_tifs(url):
    """
    Fetches an HTML page, extracts links, filters for TIF files, 
    and writes each TIF URL to a separate text file.

    Args:
        url: The URL of the HTML page to process.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <a> tags and extract href attributes
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # Filter for full URLs that end with .tif
    tif_urls = [link for link in links if link.lower().endswith('.tif')]

    # Ensure the output directory exists
    output_dir = "tif_files"
    os.makedirs(output_dir, exist_ok=True)

    for i, tif_url in enumerate(tif_urls):
        try:
            # Sanitize the URL for use as a filename (replace invalid characters)
            filename = re.sub(r'[\\/*?:"<>|]', "_", tif_url)
            filepath = os.path.join(output_dir, f"{filename}.txt")

            with open(filepath, 'w') as f:
                f.write(f"{url}{tif_url}")
            print(f"Wrote TIF URL to: {filepath}")
        except Exception as e:
            print(f"Error writing to file for URL {tif_url}: {e}")

# Example usage:
extract_links_and_filter_tifs(BASE_URL)