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

# website_links = doc.find_all('a', {'class': 'link'})

exhibit_urls = []

for link in exhibit_links:
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

# print(exhibit_urls)       # this is the list of links, see print output in console
# print(len(exhibit_urls))  # output is 1158, which is correct

company_website_url = []
company_contact = []  # IMPORTANT, REPLACE THE COMPANY LOCATION COLUMN WITH THIS INSTEAD?

for info in exhibit_urls:
#for i in range(0, 10):  # test first 20 so it doesn't take 6-7 minutes to run all 1158 items
    # company_website_url = exhibit_urls[i]
    # result = requests.get(company_website_url)
    result = requests.get(info)
    content = result.content
    doc = BeautifulSoup(content, 'html.parser')

    #  the div element with class below has website AND company headquarters information
    div_element = doc.find('div', {'class': 'col-12 col-lg-4 mb80'})

    # Finds website link below:
    span_element = div_element.find('span')  # span element within this SPECIFIC div element to find website
    if span_element == None:  # if span_element doesn't exist then there's no website link
        href_link = "No website link found"
        company_website_url.append(href_link)
    else:
        a_element = span_element.find('a')  # a tag within the span element, will throw error if no website link
        href_link = a_element.get('href')
        company_website_url.append(href_link)

    # This block of code below finds the contact information (excluding the link to company website)
    address_tag = doc.find('address')

    # if the span tag exists, then remove it
    if span_element != None:
        span_element.decompose()

    # some text formatting I grabbed from chatGPT, not sure why it works
    text_nodes = []
    for child in address_tag.children:
        text_nodes.append(child.get_text(strip=True))

    # join with an extra space between each "line" of text
    address_text = ' '.join(text_nodes)
    company_contact.append(address_text)

print(company_website_url)
print("------------------------------------")
print(company_contact)
