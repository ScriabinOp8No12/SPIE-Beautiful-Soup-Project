from bs4 import BeautifulSoup
import re

# Read the HTML file
with open('2025_1_13_308pm_MT_SPIE_MAIN.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links with those specific classes
links = soup.find_all('a', class_=['subtitle2', 'companyNameText', 'link', 'linkBlackToBlueNoUnderline'])

# Create a list to store tuples of (exhibitor_id, text, url)
exhibitor_data = []

for link in links:
    href = link.get('href', '')
    # Extract ExhibitorID from the URL using regex
    match = re.search(r'ExhibitorID=(\d+)', href)
    if match:
        exhibitor_id = int(match.group(1))  # Convert to integer for proper sorting
        exhibitor_data.append((exhibitor_id, link.text.strip(), href))

# Sort the data by ExhibitorID
sorted_data = sorted(exhibitor_data, key=lambda x: x[0])

# Save to file
with open('sorted_exhibitors.txt', 'w', encoding='utf-8') as output_file:
    for exhibitor_id, text, href in sorted_data:
        output_file.write(f"ExhibitorID: {exhibitor_id}\n")
        output_file.write(f"Company: {text}\n")
        output_file.write(f"URL: {href}\n")
        output_file.write("-" * 50 + "\n")

print(f"Saved {len(sorted_data)} exhibitors to sorted_exhibitors.txt")