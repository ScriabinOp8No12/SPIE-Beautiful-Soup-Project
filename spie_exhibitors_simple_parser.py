from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from datetime import datetime

# HOW TO USE:

# 1. Go to: https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition/exhibitors?term=&pageSize=1500
# 2. Open the inspect tool, and find the <div class="col-12">
# 3. Right click, copy -> innerHTML
# 4. Put this into the exhibitors_page.html file
# 5. Run this script -> open terminal, in root -> python spie_exhibitors_simple_parser.py
# 6. Output is in the OUTPUT_11_24_2025 folder for now

# Read HTML from local file
html_file = 'exhibitors_page_11_24_2025.html'
print(f"Reading HTML from {html_file}...")

with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Parse HTML
print("Parsing HTML...")
doc = BeautifulSoup(html_content, "html.parser")

base_url = "https://spie.org"

# Find all company name links (this is the anchor point for each company entry)
company_link_tags = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})

# Lists to store data
company_names = []
company_links = []
locations = []
booth_numbers = []
descriptions = []

print(f"Found {len(company_link_tags)} company entries. Extracting data...")

# Extract data from each company entry
for link_tag in company_link_tags:
    # Find the parent container (col-12 col-lg-5) that holds company info
    parent_col = link_tag.find_parent('div', {'class': 'col-12 col-lg-5 mb-3 mb-lg-0'})
    if not parent_col:
        # If not found, try to find the row parent
        parent_col = link_tag.find_parent('div', class_='row')
    
    # Extract company name and link
    company_name = link_tag.get_text(strip=True)
    company_href = link_tag.get('href', '')
    company_link = base_url + company_href if company_href else ''
    
    # Extract location - search in the parent column
    location_tag = None
    if parent_col:
        location_tag = parent_col.find('div', {'class': 'searchResultDescription subtext1'})
    location = location_tag.get_text(strip=True) if location_tag else ''
    
    # Extract booth number - search in the parent row container
    booth_number = ''
    if parent_col:
        parent_row = parent_col.find_parent('div', class_='row')
        if parent_row:
            booth_tag = parent_row.find('div', {'class': 'searchItemDescriptionStrong'})
            if booth_tag:
                booth_text = booth_tag.get_text(strip=True)
                # Extract booth number using regex (e.g., "Booth 5532")
                booth_match = re.search(r'Booth\s+(\d+)', booth_text)
                if booth_match:
                    booth_number = booth_match.group(1)
    
    # Extract description - search in the parent row container
    description = ''
    if parent_col:
        parent_row = parent_col.find_parent('div', class_='row')
        if parent_row:
            # Try finding by id first
            description_tag = parent_row.find('div', {'id': 'expanded'})
            if description_tag and 'presentationTwoLineAbstractText' in description_tag.get('class', []):
                description = description_tag.get_text(strip=True)
            else:
                # Try finding by class
                description_tag = parent_row.find('div', {'class': 'presentationTwoLineAbstractText hideToggleText'})
                if description_tag:
                    description = description_tag.get_text(strip=True)
    
    # Append to lists
    company_names.append(company_name)
    company_links.append(company_link)
    locations.append(location)
    booth_numbers.append(booth_number)
    descriptions.append(description)

# Create DataFrame
print("Creating DataFrame...")
df = pd.DataFrame({
    'Company Name': company_names,
    'Company Link': company_links,
    'Location': locations,
    'Booth Number': booth_numbers,
    'Description': descriptions
})

# Create OUTPUT folder if it doesn't exist
output_folder = 'OUTPUT_11_24_2025'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save to CSV with unique timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = os.path.join(output_folder, f'spie_exhibitors_WEST_{timestamp}.csv')
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"\nScraping complete!")
print(f"Total companies scraped: {len(df)}")
print(f"Data saved to: {output_file}")
print(f"\nFirst few rows:")
print(df.head())

