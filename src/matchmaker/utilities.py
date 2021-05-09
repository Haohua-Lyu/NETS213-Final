import pandas as pd
from math import floor
from scipy.spatial.distance import braycurtis
from . import data_preprocessing as DataPreprocessing

# The following codes are inspired by https://github.com/GlenCrawford/matchmaker.

# SORT ORDER
SORT_ORDER = [
    r"^age$",
    r"^sex$",
    r"^orientation$",
    r"^body_type$",
    r"^height$",
    r"^education$",
    r"^pets$",
    r"^religion$",
    r"^smokes$",
    r"^job$",
    r"^speaks$",
    r"^status$",
]

"""
Calculate the match score(s) between the input and given profile(s)
"""


def calculate_match_score(input_df, matches_df, raw=False):
    # Preprocess df and drop direct features
    if raw:
        input_df = DataPreprocessing.preprocess_input(input_df)
        matches_df = DataPreprocessing.preprocess_input(matches_df)
    input_df = input_df.drop(columns=DataPreprocessing.DIRECT_LOOKUP_FEATURES)
    matches_df = matches_df.drop(columns=DataPreprocessing.DIRECT_LOOKUP_FEATURES)

    input_vals = input_df.iloc[0].values.astype(float)

    scores = []

    # Using Bray-Curtis distance from scipy
    for _, row in matches_df.iterrows():
        row_vals = row.values.astype(float)
        d = braycurtis(input_vals, row_vals)
        scores += [floor(100 - d * 100)]

    return scores


"""
Sort the data frame (unprocessed) with given order.
"""


def sort_df(df):
    return pd.concat([df.filter(regex=reg) for reg in SORT_ORDER], axis=1)
