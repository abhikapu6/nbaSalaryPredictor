# import pandas as pd

# stats = pd.read_csv("/Users/abhik/Desktop/nba2025_with_yoe.csv")
# contracts = pd.read_csv("/Users/abhik/Desktop/contracts2025.csv")

# contracts.columns = contracts.columns.str.strip()
# contracts = contracts.rename(columns={'2024-2025': 'Salary'})


# merged = pd.merge(stats,contracts, how = "left", on = "Player")


# print(merged.to_string())
# print(merged["2024-25"].isna().sum())

from rapidfuzz import process, fuzz
import pandas as pd
import unicodedata

def normalize_name(name):
    # decompose accents, drop non-ASCII, lowercase
    nkfd = unicodedata.normalize('NFKD', name)
    ascii_only = nkfd.encode('ASCII', 'ignore').decode('ASCII')
    return ascii_only.strip().lower()
# load your files
stats     = pd.read_csv("/Users/abhik/Desktop/totals2015.csv")
contracts = pd.read_csv("/Users/abhik/Desktop/contracts2015.csv").rename(columns={'2014-15': 'Salary'})

# normalize both DataFrames
stats['nm']     = stats['Player'].apply(normalize_name)
contracts['nm'] = contracts['Player'].apply(normalize_name)

# list of normalized contract names to match against
choices = contracts['nm'].tolist()

# for each player in stats, find best match in contracts
# only accept matches with score >= threshold (e.g. 80)
threshold = 80
def get_best_match(name):
    match = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
    if match and match[1] >= threshold:
        return match[0]   # the normalized name from contracts
    else:
        return None

stats['matched_nm'] = stats['nm'].apply(get_best_match)

# now merge on the normalized+matched key
merged = (
    stats
    .merge(contracts[['nm','Salary']], 
           left_on='matched_nm', right_on='nm', 
           how='left')
    .drop(columns=['nm_x','nm_y','matched_nm'])
)
merged = merged.dropna(subset=["Salary"])
# print(merged.to_string())

merged.to_csv('/Users/abhik/Desktop/real2015.csv', index=False)
print("made final file")

