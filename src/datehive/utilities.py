import pandas as pd
import joblib
import os.path
from math import floor
from scipy.spatial.distance import braycurtis
from . import data_preprocessing as DataPreprocessing

# The following codes are inspired by https://github.com/GlenCrawford/matchmaker.

# ENCODER DIR
ENCODER_DIR = 'datehive/encoders/'

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

COLUMNS = [
        "age",
        "body_type",
        "education",
        "height",
        "job",
        "orientation",
        "pets",
        "religion",
        "sex",
        "smokes",
        "speaks",
        "status",
    ]

"""
Calculate the match score(s) between the input and given profile(s)
"""


def calculate_match_score(input_df, matches_df, raw=False):
    # Preprocess df and drop direct features
    if raw:
        input_df = DataPreprocessing.preprocess_input(input_df, use_fitted_encoder=True)
        matches_df = DataPreprocessing.preprocess_input(matches_df, use_fitted_encoder=True)
        input_df = add_religions(input_df)
        matches_df = add_religions(matches_df)
        
    candidates = filter(input_df, matches_df)
    
    input_df = input_df.drop(columns=DataPreprocessing.DIRECT_LOOKUP_FEATURES)
    matches_df = matches_df.drop(columns=DataPreprocessing.DIRECT_LOOKUP_FEATURES)

    input_vals = input_df.iloc[0].values.astype(float)

    scores = []

    # Using Bray-Curtis distance from scipy
    for i, row in matches_df.iterrows():
        if i not in candidates.index:
            scores += [0]
            continue
        row_vals = row.values.astype(float)
        d = braycurtis(input_vals, row_vals)
        scores += [floor(100 - d * 100)]

    return scores


"""
Sort the data frame (unprocessed) with given order.
"""


def sort_df(df):
    return pd.concat([df.filter(regex=reg) for reg in SORT_ORDER], axis=1)


"""
Fix columns with religions.
"""


def add_religions(df):
    religion_cols = [
        "religion_agnosticism",
        "religion_atheism",
        "religion_buddhism",
        "religion_catholicism",
        "religion_christianity",
        "religion_hinduism",
        "religion_islam",
        "religion_judaism",
        "religion_other",
        "religion_unknown",
    ]

    religions = pd.DataFrame([[0] * len(religion_cols)], columns=religion_cols)
    religions[df.iloc[:, -1].name] = df.iloc[:, -1]
    return pd.concat([df.iloc[:, :-1], religions], axis=1)


"""
Filter population based on sex & orientation
"""


def filter(input, population):
    sex = input["sex"][0]
    orientation = input["orientation"][0]

    candidates = population

    if orientation == "straight":
        candidates = candidates[candidates["sex"] == {"m": "f", "f": "m"}[sex]]
        candidates = candidates[
            candidates["orientation"].isin(["straight", "bisexual"])
        ]
    elif orientation == "gay":
        candidates = candidates[candidates["sex"] == sex]
        candidates = candidates[candidates["orientation"].isin(["gay", "bisexual"])]
    elif orientation == "bisexual":
        same_sex = candidates[candidates["sex"] == sex]
        same_sex = same_sex[same_sex["orientation"].isin(["gay", "bisexual"])]
        opposite_sex = candidates[candidates["sex"] == {"m": "f", "f": "m"}[sex]]
        opposite_sex = opposite_sex[opposite_sex["orientation"].isin(["straight", "bisexual"])]
        candidates = pd.concat([same_sex, opposite_sex])

    return candidates

def load_encoders():
    age_scaler = joblib.load(os.path.join(ENCODER_DIR, 'age_scaler.skencoder'))
    body_scaler = joblib.load(os.path.join(ENCODER_DIR, 'body_scaler.skencoder'))
    height_scaler = joblib.load(os.path.join(ENCODER_DIR, 'height_scaler.skencoder'))
    education_scaler = joblib.load(os.path.join(ENCODER_DIR, 'education_scaler.skencoder'))
    smokes_scaler = joblib.load(os.path.join(ENCODER_DIR, 'smokes_scaler.skencoder'))
    scalers = [age_scaler, body_scaler, height_scaler, education_scaler, smokes_scaler]
    ordinal_encoder = joblib.load(os.path.join(ENCODER_DIR, 'ordinal_encoder.skencoder'))
    return scalers, ordinal_encoder

def save_encoders(scalers, ordinal_encoder):
    joblib.dump(scalers[0], os.path.join(ENCODER_DIR, 'age_scaler.skencoder'))
    joblib.dump(scalers[1], os.path.join(ENCODER_DIR, 'body_scaler.skencoder'))
    joblib.dump(scalers[2], os.path.join(ENCODER_DIR, 'height_scaler.skencoder'))
    joblib.dump(scalers[3], os.path.join(ENCODER_DIR, 'education_scaler.skencoder'))
    joblib.dump(scalers[4], os.path.join(ENCODER_DIR, 'smokes_scaler.skencoder'))
    joblib.dump(ordinal_encoder, os.path.join(ENCODER_DIR, 'ordinal_encoder.skencoder'))
    return