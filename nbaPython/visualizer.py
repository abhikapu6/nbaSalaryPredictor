# import seaborn as sns
# import pandas as pd
# import matplotlib.pyplot as plt
# sns.set_style("darkgrid")

# data = pd.read_csv("/Users/abhik/Desktop/nbaData/updated2023.csv")
# sns.pairplot(data)
# plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data into a DataFrame (replace with your actual DataFrame if it's already loaded)
data = pd.read_csv("/Users/abhik/Desktop/nbaData/updated2023.csv")

# Assuming your table is already a DataFrame called 'df'

# Clean the Salary column (convert to numeric)
# df['Salary'] = df['Salary'].replace('[\$,]', '', regex=True).astype(float)

# Define the columns you want to compare against Salary (excluding non-numeric or categorical ones)
features = data.columns.drop(['Player', 'Pos'])  # Drop non-numeric/categorical columns
int_list = [int(s.replace(',', '')) for s in data["Salary"]]
data["Salary"] = int_list
data = data.sort_values(by='Salary', ascending=False)

print(data)
# Set up the figure size for multiple subplots
plt.figure(figsize=(18, 30))  # Adjust size as needed

# Loop through features and create a subplot for each
for i, col in enumerate(features, 1):
    plt.subplot(len(features)//2 + 1, 2, i)  # Adjust grid: 2 columns
    sns.scatterplot(x=data[col], y=data["Salary"])
    plt.title('Salary vs ' + str(col))
    plt.ylabel("Salary")
    plt.xlabel(str(col))
    plt.tight_layout()
plt.show()


