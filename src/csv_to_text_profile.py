import pandas as pd
from random import choices

csv_profile = pd.read_csv('./NETS213-Final/data/okcupid_clean.csv')
columns = csv_profile.columns

text = []

for i, r in csv_profile.iterrows():
    row_in_text = ''
    for c in columns[1:]:
        if r[c]:
            string = c + ': ' + str(r[c]) + ', '
            row_in_text += string
    text += [row_in_text[:-2]]
    
res = []

# ONLY DOING FIRST 100 FOR NOW
for profile in text[:100]:
    row = [profile]
    row += choices(text, k=5)
    res += [row]

res_df = pd.DataFrame(res, columns=['profile'+str(i) for i in range(1, 7)])
res_df.to_csv(r'MTURK_input.csv', index=False)
        