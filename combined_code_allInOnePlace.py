# 1. If selenium webdriver only has to load once, it should be significantly faster than doing it multiple times
# 2. Needed code / info:
# booth_numbers, company_name, exhibit_urls, description_text, company_website_url, company_contact

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

exhibits_per_page = 1500
pages = 1

main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition' \
                f'/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'


browser = webdriver.Chrome()
browser.get(main_page_url)
browser.implicitly_wait(10)
result = browser.page_source

doc = BeautifulSoup(result, "html.parser")

exhibit_links = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})
# redundant line below?
company_names = doc.find_all('a', class_='subtitle2 companyNameText link linkBlackToBlueNoUnderline')
company_descriptions = doc.find_all('div', class_='col-12 col-lg-7')


exhibit_urls = []  # done
booth_numbers = []  # done
company_name = []  # done
description_text = []  # done
company_website_url = []
company_contact = []

# Link to company page that includes: booth numbers, contact info, company website link
base_url = "https://spie.org"
for link in exhibit_links:
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

# Company Name
for name in company_names:
    names = name.text
    company_name.append(names)

# Company Description
for description in company_descriptions:
    if description.text == "":
        company_text = "No Description Found"
    else:
        company_text = description.text
    if company_text.endswith("Show full description +"):    # if text ends with "show more description +"
        company_text = company_text[:-23].strip()           # remove 22 characters from the back of the string
    description_text.append(company_text)

# Booth Number
for url in exhibit_urls:
#for i in range(1, 100):  # these 3 lines are to test a small subsection of the output so it doesn't take 6-7 minutes to run all the booth numbers once
    # booth_url = exhibit_urls[i]
    # result = requests.get(booth_url)
    result = requests.get(url)
    content = result.content
    doc = BeautifulSoup(content, 'html.parser')

    div_element = doc.find('div', {'class': 'col-12 col-lg-8 mb30'})    # finding these without using Selenium,
                                                                        # has diff class compared to if using Selenium?

    if div_element == None:
        booth_number = "No Booth Number Found"
        # print(booth_number)
        booth_numbers.append(booth_number)
    else:
        span_element = div_element.find(
            'span')  # find the span element that's within the div element of specified class above
        if span_element == None:
            booth_number = "No Booth Number Found"
            # print(booth_number)
            booth_numbers.append(booth_number)
        else:
            booth_text = span_element.text  # Find the text of the span element, which is the booth number text below
            booth_text = booth_text.strip().replace('\r\n', '')  # replaces thes "\r\n" at the end of the booth number output
            # print(booth_text) # bug testing line to see total output
            # booth_number = booth_text.split(":")[1].strip().split(" ")[0]] original code, doesn't work if more than one booth number
            # formats booth number by splitting between the : and |    is the [0] at the end needed?
            booth_number = booth_text.split(":")[1].strip().split("|")[0].rstrip()    # added .rstrip() at end to remove blank space at end of booth number output
            # print(booth_number)
            booth_numbers.append(booth_number)

    # counter += 1   # for bug testing -> print out counter with booth number output to figure out which ones are bugged
# print(booth_numbers)
# print(f"Counter is: {counter}")


