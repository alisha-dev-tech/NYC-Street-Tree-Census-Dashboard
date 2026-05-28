import pandas as pd
df = pd.read_csv('2015_Street_Tree_Census_-_Tree_Data.csv', on_bad_lines='skip', engine='python')
df_small = df.head(50000)
df_small.to_csv('2015_Street_Tree_Census_-_Tree_Data.csv', index=False)
print("Ho gaya!")