from selenium import webdriver
from bs4 import BeautifulSoup
from description_FINAL import description_text

exhibits_per_page = 1500
pages = 1

main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition' \
                f'/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'

browser = webdriver.Chrome()
browser.get(main_page_url)
browser.implicitly_wait(10)
result = browser.page_source

doc = BeautifulSoup(result, "html.parser")

company_names = doc.find_all('a', class_='subtitle2 companyNameText link linkBlackToBlueNoUnderline')

company_name = []

for name in company_names:
    names = name.text
    company_name.append(names)

# print(company_name)
# print(len(company_name))   # count of 1158 also, nice!

company_locations = doc.find_all('div', class_='searchResultDescription subtext1')

company_location = []

# counter = 0
for company in company_locations:
    location = company.text
    company_location.append(location)
    # print(location, counter)
    # counter+=1

# print(company_location)

# print(company_location, counter)
# print(len(company_location))   # count of 1158 as well, nice!

name_location_description = []


for i in range (len(company_name)):
    info = company_name[i] + " | Location: " + company_location[i] + " | " + description_text[i]
    name_location_description.append(info)

# print(name_location_description)