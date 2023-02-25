import pandas as pd
from description_FINAL import description_text
from name_location_description_FINAL import company_name, company_location
from boothNum_FINAL import booth_numbers
from booth_links_FINAL import exhibit_urls
from company_contact_and_website import company_website_url, company_contact
#from company_contact_info_test import company_contact

data = {
    # Add index column here, or excel just works?
    'Booth Number(s)': booth_numbers,
    'Company Name': company_name,
    # 'Link to Company': exhibit_urls,   # working, but doesn't isn't clickable
    'Link to Company': ['=HYPERLINK("{}")'.format(url) for url in exhibit_urls],
    'Description': description_text,
    'Notes': None,
    'Website link': ['=HYPERLINK("{}")'.format(url) for url in company_website_url],
    'Company Contact Information': company_contact,

    # 'Location': company_location,
}

# create the dataframe
df = pd.DataFrame(data)

# convert dataframe to csv
df.to_csv(r'C:\Users\nharw\Desktop\SPIE_West_Revised3.csv', index=False)

# REMEMBER: In the CSV output when opened in Excel, the booth numbers are hiding due to a single bug
# Company description somehow drags onto the booth number!
# Fix: Click the booth number column, then click "align left"!