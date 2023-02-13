from bs4 import BeautifulSoup
import requests
import json

#  For the main_page_url below
# 1. We can change the default "pageSize=50" to "pageSize=5000", this will show 5000 exhibitors per page instead of 50 exhibitors per page
# 2. Alternatively, we can change the default "pagesVisited=1" to "pagesVisited=50" this will load 50 pages worth of 50 exhibitors per page
# 3. Total number of Exhibits for (2022?) was 1158, so either method should work

exhibits_per_page = 550  # if I do a bit more than 550, the pycharm output won't have 2b-special (first exhibitor)
                         # hard to bug check when I can't ctrl F in the output to see if it's working or not.
                         # I think it cuts off once the output is too large, and it won't show the earlier exhibitors
pages = 1
main_page_url = f'https://spie.org/conferences-and-exhibitions/photonics-west/exhibitions/photonics-west-exhibition/exhibitors?term=&pageSize={exhibits_per_page}&pagesVisited={pages}&sortBy=Relevance'

result = requests.get(main_page_url)

doc = BeautifulSoup(result.text, "html.parser")

# print(doc.prettify())
app_div = doc.find("div", {"id": "new"}).find("div", {"id": "app"})
print(app_div)

# description = doc.select_one("#expanded").text
#
# print(description)

# json_data = doc.find("div", {"id": "new"}).find("div", {"id": "app"}).get("propsdata")
#
# parsed_json = json.loads(json_data)
#
# # Accessing the description
# description = parsed_json["Items"][0]["Description"]
# print(description)








