from bs4 import BeautifulSoup
import requests

booth_2_test = 'https://spie.org/ExhibitorDetail?ExpoID=2100&ExhibitorID=53840'
result = requests.get(booth_2_test)


content = result.content
doc = BeautifulSoup(content, 'html.parser')

div_element = doc.find('div', {'class': 'col-12 col-lg-8 mb30'})
assert div_element is not None, "Can't find div element"

span_element = div_element.find('span')  # find the span element that's within the div element of specified class above
assert span_element is not None, "Can't find span element"

booth_text = span_element.text  # Find the text of the span element, which is the booth number text below
assert booth_text is not None, "Can't find booth number"

booth_number = booth_text.split(":")[1].strip().split(" ")[0] # formats booth number properly so we can print it out
print("Booth Number:", booth_number)





