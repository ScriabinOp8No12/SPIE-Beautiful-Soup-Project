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

# company_descriptions = doc.find_all('div', class_='presentationTwoLineAbstractText hideToggleText')
company_descriptions = doc.find_all('div', class_='col-12 col-lg-7')

description_text = []
# counter = 0   # bug testing line

for description in company_descriptions:
    if description.text == "":
        company_text = "No Description Found"
    else:
        company_text = description.text
    if company_text.endswith("Show full description +"):    # if text ends with "show more description +"
        company_text = company_text[:-23].strip()           # remove 22 characters from the back of the string
    description_text.append(company_text)

    # print(company_text, counter)  # bug testing lines
    # counter += 1                  # bug testing lines

# print(description_text)
# print(len(description_text))  # count of 1158, nice!



