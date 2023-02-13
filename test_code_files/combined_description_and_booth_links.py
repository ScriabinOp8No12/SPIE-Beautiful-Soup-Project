from selenium import webdriver
from bs4 import BeautifulSoup

exhibits_per_page = 1500
pages = 1

main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition' \
                f'/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'

browser = webdriver.Chrome()
browser.get(main_page_url)
browser.implicitly_wait(10)
result = browser.page_source

# parse using beautiful soup
doc = BeautifulSoup(result, "html.parser")

# can't do doc.find_all().text because you can't use .text on a list of elements,
# it only works if you do doc.find().text (which is on one element)

company_descriptions = doc.find_all('div', class_='presentationTwoLineAbstractText hideToggleText')

# Find all the exhibit links on the page using the <a> tag and class
exhibit_links = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})

base_url = "https://spie.org"
exhibit_urls = []

for link in exhibit_links:
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

description_text = []

for description in company_descriptions:
    company_text = description.text
    description_text.append(company_text)

