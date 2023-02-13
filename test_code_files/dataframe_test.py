import pandas as pd

data = {
    'name': ['Nathan', 'Matthew', 'Mom', 'Dad'],
    'location': ['Broomfield, Colorado', 'Broomfield, Colorado', 'Boulder, Colorado', 'Boulder, Colorado'],
    'description': ['this is a long description to test how the table structure looks when it wraps',
                    'this will also be really long so that I can test this', 'this is short', 'this is also short'],
    'favorite number': ['2342', '93480, 234980', '832', '12039']
}

# create the dataframe
df = pd.DataFrame(data)

# To see output
# print(df)

# convert dataframe to csv
df.to_csv(r'C:\Users\nharw\Desktop\dataframe_test_1.csv', index=False)
