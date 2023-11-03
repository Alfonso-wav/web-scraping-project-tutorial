# import all libraries
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import sqlite3 as sq
import matplotlib.pyplot as plt
import seaborn as sns

# store web in variable
url =  'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

# request webs code
tesla_revenue = requests.get(url, time.sleep(10)).text


# If not information is extracted, then connect as anonymous
if "403 Forbidden" in tesla_revenue:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    request = requests.get(url, headers = headers)
    time.sleep(10)
    tesla_revenue = request.text

# display the code
# print(tesla_revenue)

# store in variable the parser in order to work with the code
soup = bs(tesla_revenue, "html.parser")

# display to confirm
# print(soup)

# find all tables in which the target is stored
tables = soup.find_all("table", class_ = "historical_data_table table")

# display to confirm

# print(tables)

# iterate the tables to get the target table index
for index,table in enumerate(tables):
    if "Tesla Quarterly Revenue" in str(table):
        table_index = index
        break

# store in variable the target table
quarterly_table = tables[table_index]

# display to confirm
print(quarterly_table)

# create an empty list
list_ = []

# iterate through target table to create a list object
for td in quarterly_table.find_all('td'):
    list_.append(td.text)

# print the list to confirm        
# print(list_)

# create empty list to store values
date = []
dollars = []

# iterate  twice through the list to separate the values into both lists
for i in range(0, len(list_),2):
    date.append(list_[i])
    
for i in range(1, len(list_),2):
    dollars.append(list_[i])

# print both lists to confirm   
# print(date)
# print(dollars)

# convert the lists into a dataframe with pandas
df = pd.DataFrame({'Dates': date, 'Price' : dollars })

# print first items to confirm
# print(df.head())

# delete the signs and commas of the price column 
df['Price'] = df['Price'].astype(str).str.replace('$', '').str.replace(',', '')

# print to confirm
# print(df.head())

# replace empty values with 'nan'
df = df.replace('', float('nan'))

# drop the na form table
df = df.dropna()

# print to confirm
# print(df.tail())

# # create connection with sqlite3 
# con = sq.connect('tesla.db')

# # convert the dataframe into sql and name it
# df.to_sql('quarterly_rev', con)

# con.commit()
# con.close()