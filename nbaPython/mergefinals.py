import pandas as pd

years = [2016,2017,2018,2019,2020,2021,2022,2023,2025]

data = pd.read_csv("/Users/abhik/Desktop/nbaData/updated2015.csv",index_col=0)

# curr = pd.read_csv("/Users/abhik/Desktop/nbaData/updated2015.csv",index_col=0)
# df = pd.read_csv("nba.csv", index_col=0)

for x in years:
    curr = pd.read_csv("/Users/abhik/Desktop/nbaData/updated" + str(x) + ".csv",index_col=0)
    data = pd.concat([data,curr],ignore_index=True)

data["Salary"] = (
    data["Salary"]
    .astype(str)                      # make sure it's string
    .str.replace(",", "", regex=False)
    .astype(float)
)

print(data)


data.to_csv("/Users/abhik/Desktop/nbaData/masterData1.csv")
print("made master file")