import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
import time
from datetime import datetime
import json

def save_progress(data_dict, suffix='checkpoint'):
    """Save current progress to both CSV and JSON formats"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save as JSON (this will always work, even if lists are different lengths)
    json_file = f'SPIE_WEST_{suffix}_{timestamp}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=2)

    # Try to save as CSV
    try:
        df = pd.DataFrame(data_dict)
        csv_file = f'SPIE_WEST_{suffix}_{timestamp}.csv'
        df.to_csv(csv_file, index=False)
        print(f"Saved to both {json_file} and {csv_file}")
    except ValueError as e:
        print(f"Could not create CSV due to uneven lengths. Data saved to {json_file}")
        print(f"Error: {str(e)}")


print("There are 6 progress bars, only the 4th one takes a long time!")
print(f"Selenium version: {selenium.__version__}")

doc = None
browser = None

try:
    # Create Chrome options for browser initialization
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize browser
    browser = webdriver.Chrome(options=options)
    print("Browser initialized successfully!")

    # Set up pagination parameters for the main exhibitors page
    exhibits_per_page = 50
    pages = 40

    # Main exhibitors page URL that contains all company links
    main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'
    # BIOS exhibitors BELOW, uncomment below, and comment out above to run that one
    # main_page_url = 'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/bios-expo/exhibitors?term=&pageSize=50&pagesVisited=10&sortBy=Relevance'

    # Get the main page content (this is just ONE request)
    browser.get(main_page_url)
    browser.implicitly_wait(20)
    result = browser.page_source

    doc = BeautifulSoup(result, "html.parser")

except Exception as e:
    print(f"Error type: {type(e)}")
    print(f"Error details: {str(e)}")

# Find all company links and descriptions from the main page
exhibit_links = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})
company_descriptions = doc.find_all('div', class_='col-12 col-lg-7')

# Initialize lists for storing data
exhibit_urls = []  # URLs to individual company pages
company_name = []  # Company names
description_text = []  # Company descriptions

# Base URL for building complete links
base_url = "https://spie.org"

# PROGRESS BAR 1: Collect all exhibit URLs (instant - just parsing the main page)
for link in tqdm(exhibit_links, position=0, desc="Collecting URLs"):
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

# PROGRESS BAR 2: Collect company names (instant - parsing main page data)
for name in tqdm(exhibit_links, position=0, desc="Collecting names"):
    names = name.text
    company_name.append(names)

# PROGRESS BAR 3: Collect descriptions (instant - parsing main page data)
for description in tqdm(company_descriptions, position=0, desc="Collecting descriptions"):
    if description.text == "":
        company_text = "No Description Found"
    else:
        company_text = description.text
    if company_text.endswith("Show full description +"):
        company_text = company_text[:-23].strip()
    description_text.append(company_text)

# Pre-fill the lists that will be updated with placeholders to ensure consistent lengths
total_companies = len(exhibit_urls)
booth_numbers = ["Pending"] * total_companies
company_website_url = ["Pending"] * total_companies
company_contact = ["Pending"] * total_companies

# PROGRESS BAR 4: Process individual company pages (slow - requires 10s delay between requests because we are accessing
# the exhibitor's specific page and extracting the booth number and other info)
checkpoint_interval = 10  # Save progress every 10 companies
try:
    for i, url in enumerate(tqdm(exhibit_urls, position=0, desc="Processing company pages")):
        try:
            # Make request to individual company page
            result = requests.get(url, stream=True)
            content = result.content
            doc = BeautifulSoup(content, 'html.parser')

            # Extract booth number information
            div_element_booth = doc.find('div', {'class': 'col-12 col-lg-8 mb30'})
            booth_number = "No Booth Number Found"
            if div_element_booth:
                span_element_booth = div_element_booth.find('span')
                if span_element_booth:
                    booth_text = span_element_booth.text.strip().replace('\r\n', '')
                    try:
                        booth_number = booth_text.split(":")[1].strip().split("|")[0].rstrip()
                    except IndexError:
                        booth_number = "Booth Number Format Error"
            booth_numbers[i] = booth_number

            # Extract contact info and website
            div_element_contact_info = doc.find('div', {'class': 'col-12 col-lg-4 mb80'})
            website_link = "No website link found"
            contact_info = "No Contact Info Found"

            # Replace the contact info processing section with this:
            if div_element_contact_info:
                span_element_contact_info = div_element_contact_info.find('span')
                if span_element_contact_info:
                    # Get website link first
                    a_element = span_element_contact_info.find('a')
                    if a_element:
                        website_link = a_element.get('href')
                        # Remove the website text from span
                        website_text = span_element_contact_info.find('a').extract()

                    # Remove any "Website: " text that might remain
                    for text in span_element_contact_info.find_all(text=True):
                        if 'Website:' in text:
                            text.replace_with(text.replace('Website:', '').strip())

                    # Get contact info (now without website)
                    contact_info = span_element_contact_info.text.strip()

                    # Process address
                    span_element_contact_info.decompose()
                    address_tag = doc.find('address')
                    if address_tag:
                        text_nodes = [child.get_text(strip=True) for child in address_tag.children]
                        address_text = ' '.join(text_nodes)
                        # Only add address text if contact_info is empty or different
                        if not contact_info or address_text != contact_info:
                            contact_info = f"{contact_info} {address_text}".strip()

            # Update values by index instead of appending
            company_website_url[i] = website_link
            company_contact[i] = contact_info

            # Save checkpoint periodically
            if (i + 1) % checkpoint_interval == 0:
                current_data = {
                    'Booth Number(s)': booth_numbers,
                    'Company Name': company_name,
                    'Link to Company': exhibit_urls,
                    'Description': description_text,
                    'Website link': company_website_url,
                    'Company Contact Information': company_contact
                }
                save_progress(current_data, f'checkpoint_{i + 1}')

            # 10-second delay between requests as per robots.txt
            time.sleep(10)

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            # Placeholder values will remain in place for this company
            time.sleep(10)  # Still maintain delay even after error

except Exception as e:
    print(f"Major error in processing: {str(e)}")
    save_progress({
        'Booth Number(s)': booth_numbers,
        'Company Name': company_name,
        'Link to Company': exhibit_urls,
        'Description': description_text,
        'Website link': company_website_url,
        'Company Contact Information': company_contact
    }, 'error_backup')

# PROGRESS BAR 5 & 6: Create final DataFrame with formatting (instant)
try:
    final_data = {
        'Booth Number(s)': booth_numbers,
        'Company Name': company_name,
        'Link to Company': ['=HYPERLINK("{}")'.format(url) for url in
                            tqdm(exhibit_urls, desc="Formatting company links")],
        'Description': description_text,
        'Website link': ['=HYPERLINK("{}")'.format(url) if url != "No website link found" and url != "Pending"
                         else url for url in tqdm(company_website_url, desc="Formatting website links")],
        'Company Contact Information': company_contact
    }

    # Save final files in multiple formats
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save as JSON
    with open(f'SPIE_WEST_final_{timestamp}.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    # Save as CSV and Excel
    df = pd.DataFrame(final_data)
    df.to_csv(f'SPIE_WEST_final_{timestamp}.csv', index=False)
    df.to_excel(f'SPIE_WEST_final_{timestamp}.xlsx', index=False)

except Exception as e:
    print(f"Error in final save: {str(e)}")

finally:
    if browser:
        browser.quit()