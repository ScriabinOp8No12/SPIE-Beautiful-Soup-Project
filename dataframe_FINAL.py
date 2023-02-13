import pandas as pd
from description_FINAL import description_text
from name_location_description_FINAL import company_name, company_location
from booths_FINAL import booth_numbers

data = {
    'Name': company_name,
    'Location': company_location,
    'Description': description_text,
    'Booth Number(s)': booth_numbers,
}

# create the dataframe
df = pd.DataFrame(data)

# convert dataframe to csv
df.to_csv(r'C:\Users\nharw\Desktop\SPIE_West_Output_1.csv', index=False)

# REMEMBER: In teh CSV output when opened in Excel, the booth numbers are hiding!
# Click the booth number column, then click "align left"!