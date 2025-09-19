import pandas as pd

table = pd.read_csv("/Users/abhik/Desktop/nbaData/updated2025.csv")
salaries = table["Salary"]
print(salaries)
salaries = [x[1:] for x in salaries]

infSalaries = [x.replace(',', '') for x in salaries]
infSalaries = [(int(x) * 1.00) for x in infSalaries]
infSalaries = [int(x) for x in infSalaries]
infSalaries = ["{:,}".format(x) for x in infSalaries]

table["Salary"] = infSalaries
print(table)

table.to_csv("/Users/abhik/Desktop/2updated2025.csv")
print("I made the file")