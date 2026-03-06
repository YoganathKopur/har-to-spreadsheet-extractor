import json
import csv
from urllib.parse import urlparse

# --- Configuration ---
# Make sure your exported HAR file is named exactly this, 
# or change this variable to match your file's name.
HAR_FILE_PATH = "sample_data.har"
CSV_OUTPUT_PATH = 'api_mapping.csv'

def extract_api_calls():
    try:
        with open(HAR_FILE_PATH, 'r', encoding='utf-8') as f:
            har_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {HAR_FILE_PATH}. Make sure it's in the same folder as this script.")
        return

    # Columns matching your Google Sheet structure
    headers = ['Module', 'Sub-module/Tab', 'Another Sub-module', 'Type', 'API', 'Payload']
    
    with open(CSV_OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Loop through all recorded network requests
        for entry in har_data['log']['entries']:
            request = entry['request']
            url = request['url']
            
            # Filter to only include your specific API calls
            # CHANGE 'example.com' TO YOUR TARGET DOMAIN WHEN RUNNING LOCALLY
            if '/api/' in url and 'example.com' in url:
                method = request['method']
                
                # Extract payload for POST/PUT requests
                payload = ""
                if 'postData' in request and 'text' in request['postData']:
                    payload = request['postData']['text']
                
                # Attempt to guess the Module based on the URL path 
                path_parts = urlparse(url).path.split('/')
                module = path_parts[2] if len(path_parts) > 2 else ""
                sub_module = path_parts[3] if len(path_parts) > 3 else ""
                
                # Format the URL as a Google Sheets hyperlink formula
                clickable_link = f'=HYPERLINK("{url}", "{url}")'
                
                # Write the row
                writer.writerow([module.capitalize(), sub_module.capitalize(), '', method, clickable_link, payload])
                
    print(f"Success! Extracted API calls to {CSV_OUTPUT_PATH}")

if __name__ == '__main__':
    extract_api_calls()