import pandas as pd

url = "https://www.basketball-reference.com/leagues/NBA_2015_advanced.html"
info = pd.read_csv("/Users/abhik/Desktop/info2015_with_yoe.csv")
tables = pd.read_html(url)
stats = tables[0]

stats = stats[["Player","BPM","VORP","WS/48"]]
stats.drop(index=stats.index[-1],axis=0,inplace=True)
stats = stats[stats.duplicated(subset='Player', keep='first') == False]
stats.reset_index(drop=True, inplace=True)



merged = pd.merge(info,stats,how = "inner", on =  "Player", )
# merged = merged.sort_values(by='VORP', ascending=False)
merged.reset_index(drop=True, inplace=True)

# print(merged)
merged.to_csv('/Users/abhik/Desktop/totals2015.csv', index=False)
print("Made the totals file")


