# 1. If selenium webdriver only has to load once, it should be significantly faster than it loading multiple times
# 2. Needed code / info:
# booth_numbers, company_name, exhibit_urls, description_text, company_website_url, company_contact
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

print("There are 6 progress bars, the 4th one takes the longest, and the others are basically instant!")
print(f"Selenium version: {selenium.__version__}")

doc = None
browser = None

try:
    # Create Chrome options once (removed duplicate options creation)
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialize browser
    browser = webdriver.Chrome(options=options)
    print("Browser initialized successfully!")

    exhibits_per_page = 50
    pages = 40

    # main_page_url = 'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/bios-expo/exhibitors?term=&pageSize=50&pagesVisited=10&sortBy=Relevance'
    main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'

    browser.get(main_page_url)
    browser.implicitly_wait(10)
    result = browser.page_source

    doc = BeautifulSoup(result, "html.parser")

except Exception as e:
    print(f"Error type: {type(e)}")
    print(f"Error details: {str(e)}")
# exhibit links are derived by clicking on the company name (they have the name of the company as the url text!)
exhibit_links = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})
# redundant line below since they use the same part of the html
# company_names = doc.find_all('a', class_='subtitle2 companyNameText link linkBlackToBlueNoUnderline')
company_descriptions = doc.find_all('div', class_='col-12 col-lg-7')

exhibit_urls = []  # done
company_name = []  # done
description_text = []  # done

booth_numbers = []  # done
company_website_url = []  # done
company_contact = []  # done

# Link to company page that includes: booth numbers, contact info, company website link
base_url = "https://spie.org"
# Adding tqdm for all loops
for link in tqdm(exhibit_links, position=0):
    # print statement here to check progress
    # print('current link', link)
    # for i in tqdm (range(len(exhibit_links)))
    # link = exhibit_links[i]
    # exhibit_url = base_url + link['href']
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

# Company Name  (modified the below from for name in company_names  --> to "for name in exhibit_links:" )
for name in tqdm(exhibit_links, position=0):
    names = name.text
    company_name.append(names)

# Company Description
for description in tqdm(company_descriptions, position=0):
    if description.text == "":
        company_text = "No Description Found"
    else:
        company_text = description.text
    if company_text.endswith("Show full description +"):    # if text ends with "show more description +"
        company_text = company_text[:-23].strip()           # remove 22 characters from the back of the string
    description_text.append(company_text)

for url in tqdm(exhibit_urls, position=0):
    try:
        result = requests.get(url, stream=True)
        content = result.content
        doc = BeautifulSoup(content, 'html.parser')

        # Extract booth number div
        div_element_booth = doc.find('div', {'class': 'col-12 col-lg-8 mb30'})

        if div_element_booth is None:
            booth_number = "No Booth Number Found"
            booth_numbers.append(booth_number)
            print(f"Booth info missing for URL: {url}")  # Debugging output
        else:
            span_element_booth = div_element_booth.find('span')
            if span_element_booth is None:
                booth_number = "No Booth Number Found"
                booth_numbers.append(booth_number)
                print(f"No span found in booth info for URL: {url}")  # Debugging output
            else:
                booth_text = span_element_booth.text.strip().replace('\r\n', '')
                try:
                    # Attempt to extract booth number using split
                    booth_number = booth_text.split(":")[1].strip().split("|")[0].rstrip()
                except IndexError:
                    booth_number = "Booth Number Format Error"  # Handle unexpected format
                    print(f"Unexpected booth number format for URL: {url}, text: {booth_text}")
                booth_numbers.append(booth_number)

        # Extract company contact info div
        div_element_contact_info = doc.find('div', {'class': 'col-12 col-lg-4 mb80'})
        if div_element_contact_info is None:
            print(f"Contact info missing for URL: {url}")
            company_contact.append("No Contact Info Found")
        else:
            span_element_contact_info = div_element_contact_info.find('span')
            if span_element_contact_info is None:
                print(f"No span found in contact info for URL: {url}")
                company_contact.append("No Contact Info Found")
            else:
                contact_info_text = span_element_contact_info.text.strip()
                company_contact.append(contact_info_text)

    except Exception as e:
        print(f"Error processing URL: {url}")
        print(f"Error details: {str(e)}")

    # Finds website link below:
    span_element_contact_info = div_element_contact_info.find('span')  # span element within this SPECIFIC div element to find website
    if span_element_contact_info == None:  # if span_element doesn't exist then there's no website link
        href_link = "No website link found"
        company_website_url.append(href_link)
    else:
        a_element = span_element_contact_info.find('a')  # a tag within the span element, will throw error if no website link
        href_link = a_element.get('href')
        company_website_url.append(href_link)

    # Finds contact / location information (excluding the link to company website)
    address_tag = doc.find('address')

    # if the span tag exists, then remove it
    if span_element_contact_info != None:
        span_element_contact_info.decompose()

    # some text formatting I grabbed from chatGPT, not sure why it works
    text_nodes = []
    for child in address_tag.children:
        # don't use tqdm here because it'll get confused since this is within the outer for loop!
        text_nodes.append(child.get_text(strip=True))

    # join with an extra space between each "line" of text
    address_text = ' '.join(text_nodes)
    company_contact.append(address_text)

# Output to CSV (panda dataframe below)
# modified for list comprehension to use tqdm too
data = {
    # Add index column here, or excel just works?
    'Booth Number(s)': booth_numbers,
    'Company Name': company_name,
    'Link to Company': ['=HYPERLINK("{}")'.format(url) for url in tqdm(exhibit_urls, position=0)],
    'Description': description_text,
    'Notes': None,
    'Website link': ['=HYPERLINK("{}")'.format(url) for url in tqdm(company_website_url, position=0)],
    'Company Contact Information': company_contact,

}

# create the dataframe
df = pd.DataFrame(data)

# convert dataframe to csv
df.to_csv(r'C:\Users\nharw\Desktop\SPIE_WEST_1_2_2025_v3_TEST.csv', index=False)

# convert csv to .xlsx afterward to save the formatting, otherwise the links aren't clickable, and the columns reset

