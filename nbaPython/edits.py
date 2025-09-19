import pandas as pd

df = pd.read_csv("/Users/abhik/Desktop/nba2025_with_yoe.csv")

df.fillna(0, inplace=True)

df.to_csv("/Users/abhik/Desktop/nba2025_with_yoe1.csv", index=False)

print("We did it") 

