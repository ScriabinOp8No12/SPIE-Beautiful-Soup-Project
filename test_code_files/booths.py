# NOT WORKING CODE

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

base_url = "https://spie.org"
exhibit_links = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})

exhibit_urls = []

for link in exhibit_links:
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

# print(exhibit_urls)       # this is the list of links, see print output in console
# print(len(exhibit_urls))  # output is 1158, which is correct

booth_numbers = []
counter = 0

# for url in exhibit_urls:
for i in range(428, 440):
    booth_url = exhibit_urls[i]
    browser = webdriver.Chrome()
    browser.get(main_page_url)
    browser.implicitly_wait(10)
    result = browser.page_source
    doc = BeautifulSoup(result, "html.parser")

    booth_info = doc.find('span')
    if booth_info == None:
        booth_number = "No Booth Number Found"
        booth_numbers.append(booth_number)
    else:
        booth_text = booth_info.text.strip()
        booth_number = booth_text.split(":")[1].strip()
        booth_numbers.append(booth_number)

    counter += 1
    print(booth_number)  # for seeing if booth numbers are getting stored properly
    print(f"Counter is: {counter}")


    # if div_element == None:
    #     booth_number = "No Booth Number Found"
    #     booth_numbers.append(booth_number)
    # else:
    #     span_element = div_element.find(
    #         'span')  # find the span element that's within the div element of specified class above
    #     if span_element == None:
    #         booth_number = "No Booth Number Found"
    #         booth_numbers.append(booth_number)
    #     else:
    #         booth_text = span_element.text  # Find the text of the span element, which is the booth number text below
    #         booth_number = booth_text.split(":")[1].strip().split(" ")[0]  # formats booth number properly
    #         booth_numbers.append(booth_number)



