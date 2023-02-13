from selenium import webdriver
from bs4 import BeautifulSoup

#  For the main_page_url below
# 1. We can change the default "pageSize=50" to "pageSize=1500", this will show 1500 exhibitors per page instead of 50 exhibitors per page
# 2. Alternatively, we can change the default "pagesVisited=1" to "pagesVisited=50" this will load 50 pages worth of 50 exhibitors per page
# 3. Total number of Exhibits for (2022?) was 1158, so either method will work

# if I do a bit more than 550, the pycharm output won't have 2b-special (first exhibitor)
# hard to bug check when I can't ctrl F in the output to see if it's working or not.
# I think it cuts off once the output is too large, and it won't show the earlier exhibitors

exhibits_per_page = 1500
pages = 1

main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition' \
                f'/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'

# Start a new instance of Chrome
browser = webdriver.Chrome()

# Open the URL
browser.get(main_page_url)

# Wait for the page to load, if it takes longer than 10 seconds, and it can't find the page, throw an exception/error
browser.implicitly_wait(10)

# Get the page source
result = browser.page_source

# Parse the page source using BeautifulSoup
doc = BeautifulSoup(result, "html.parser")

base_url = "https://spie.org"

# Find all the exhibit links on the page using the <a> tag and class
exhibit_links = doc.find_all('a', {'class': 'subtitle2 companyNameText link linkBlackToBlueNoUnderline'})

# Loop through the exhibit links to get the URL of each exhibit
exhibit_urls = []
for link in exhibit_links:
    exhibit_url = base_url + link['href']
    exhibit_urls.append(exhibit_url)

print(exhibit_urls)       # this is the list of links, see print output in console
print(len(exhibit_urls))  # output is 1158, which is correct
