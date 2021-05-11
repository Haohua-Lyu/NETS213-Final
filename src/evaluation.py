import re
import pandas as pd
import numpy as np
from datehive import utilities as Utilities

def split(s):
    res = re.split('age: |, body_type: |, education: |, height: |, job: |, orientation: |, pets: |, religion: |, sex: |, smokes: |, speaks: |, status: ', s)
    res = [np.nan if attr == 'nan' else attr for attr in res[1:]]
    res[0] = int(res[0])
    res[3] = float(res[3])
    return res

mturk_results = pd.read_csv(r'../data/QC_output_HIT.csv')

confusion = [[0, 0], [0, 0]]

for _, row in mturk_results.iterrows():
    profile_a = split(row['0'])
    profile_b = split(row['1'])
    a_df = pd.DataFrame([profile_a], columns = Utilities.COLUMNS)
    b_df = pd.DataFrame([profile_b], columns = Utilities.COLUMNS)
    label = row['2']
    if len(Utilities.filter(a_df, b_df)) == 0 and label == 'match':
        continue
    predict = 'match' if Utilities.calculate_match_score(a_df, b_df, raw=True)[0] > 50 else 'notmatch'
    if predict == 'match' and label == 'match':
        confusion[0][0] += 1
    elif predict == 'match' and label == 'notmatch':
        confusion[0][1] += 1
    elif predict == 'notmatch' and label == 'match':
        confusion[1][0] += 1
    elif predict == 'notmatch' and label == 'notmatch':
        confusion[1][1] += 1
    
precision = confusion[0][0] / (confusion[0][0] + confusion[0][1])
recall = confusion[0][0] / (confusion[0][0] + confusion[1][0])
f1 = 2 * (precision*recall) / (precision + recall)
print('precision:', precision)
print('recall:', recall)
print('f1:', f1)
print('confusion:', confusion)