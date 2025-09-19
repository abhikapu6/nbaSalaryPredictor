# import requests
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time

import pandas as pd


# Load the per-game stats for the 2024 season (adjust if needed)
url = 'https://www.basketball-reference.com/leagues/NBA_2015_per_game.html'
# Load all tables on the page
tables = pd.read_html(url)

# Per-game stats should be the first table
df = tables[0]

# Remove duplicate header rows
df = df[df['Player'] != 'Player']

# Reset index
df.reset_index(drop=True, inplace=True)

# Convert numeric columns (like PTS) to proper float values
df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')

# Sort by PPG descending
# df = df.sort_values(by='PER', ascending=False)

df.drop(index=df.index[-1],axis=0,inplace=True)
df = df[df.duplicated(subset='Player', keep='first') == False]
# Print top scorers

realData = pd.DataFrame()

realData = df[['Player', 'Age', 'Pos',"GS"]]

realData.reset_index(drop=True, inplace=True)

realData.to_csv('/Users/abhik/Desktop/info2015.csv', index=False)
print("info File made")
# print(realData)
# print(df)



# for _, row in realData.iterrows(): 
#     print(f"{row['Player']} ({row['Age']}) – Position: {row["Pos"]} - Games Played: {row["GS"]}")

# print(df)



