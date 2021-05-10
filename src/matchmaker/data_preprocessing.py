import numpy as np
import pandas as pd
import sklearn.preprocessing as sk
from . import utilities as Utilities

# The following codes are inspired by https://github.com/GlenCrawford/matchmaker.

# INPUT
# INPUT_PATH = "/data/okcupid_clean.csv"
INPUT_PATH = "../data/okcupid_clean.csv"

INPUT_COLS_TO_USE = [
    "age",
    "body_type",
    "education",
    "height",
    "orientation",
    "pets",
    "religion",
    "sex",
    "smokes",
]

DIRECT_LOOKUP_FEATURES = ["sex", "orientation"]

# SCALES
COLS_TO_SCALE = ["age", "body_type", "height", "education", "smokes"]

AGE_SCALE = (0, 5)
BODY_TYPE_SCALE = (0, 0.4)
HEIGHT_SCALE = (0, 0.4)
EDUCATION_SCALE = (0, 0.5)
SMOKES_SCALE = (0, 3)
RELIGION_SCALE = 0.5
PETS_SCALE = {False: 0, True: 0.2}

# CATEGORICAL FEATURES TO PREDEFINED (AND CONSOLIDATED) ORDINALITIES
COLS_TO_ORDINAL_ENCODE = ["body_type", "education", "smokes"]

BODY_TYPE_ORDINALITIES = [
    "thin",
    "fit",
    "average",
    "curvy",
    "overweight",
]
EDUCATION_ORDINALITIES = [
    "less_than_high_school",
    "high_school",
    "undergraduate_in_progress",
    "completed_undergraduate_study",
    "graduate_in_progress",
    "completed_graduate_study",
]
SMOKES_ORDINALITIES = [
    "no",
    "buffer1",
    "sometimes",
    "buffer2",
    "yes",
]

"""
Load input from INPUT_PATH.
"""


def load_input(for_processing=True):
    if for_processing:
        return pd.read_csv(INPUT_PATH, usecols=INPUT_COLS_TO_USE)
    return Utilities.sort_df(pd.read_csv(INPUT_PATH))


"""
Preprocess input data to convert all attributes into numerical values (so they can be trained using KNN).
"""


def preprocess_input(df=None, use_fitted_encoder=False):
    if df is None:
        df = load_input()
    else:
        df = df[INPUT_COLS_TO_USE]

    # Initialize encoders
    scalers, ordinal_encoder = initialize_encoders(use_fitted_encoder)

    # Consolidates the values
    df = consolidate_values(df)

    # Creates two columns for pets: cats/dogs, apply the scales, and drops the original one
    df["pets_cats"] = df["pets"].str.contains("cats")
    df["pets_dogs"] = df["pets"].str.contains("dogs")
    df = df.replace({"pets_cats": PETS_SCALE, "pets_dogs": PETS_SCALE})
    df.drop("pets", axis=1, inplace=True)

    # Similarly, create multiple dummy cols for religion, apply scales, and drops the original one
    religions = pd.get_dummies(df["religion"], prefix="religion")
    religions[religions == 1] = RELIGION_SCALE
    df = pd.concat([df, religions], axis=1)
    df.drop("religion", axis=1, inplace=True)

    # Apply ordinal encoding
    if not use_fitted_encoder:
        ordinal_encoder.fit(df[COLS_TO_ORDINAL_ENCODE])
        
    df[COLS_TO_ORDINAL_ENCODE] = ordinal_encoder.transform(df[COLS_TO_ORDINAL_ENCODE])

    # Apply scaling
    for i in range(len(COLS_TO_SCALE)):
        if not use_fitted_encoder:
            scalers[i].fit(df[[COLS_TO_SCALE[i]]])
        df[[COLS_TO_SCALE[i]]] = scalers[i].transform(df[[COLS_TO_SCALE[i]]])

    Utilities.save_encoders(scalers, ordinal_encoder)
    
    # Remove NaN
    df[df.height.isnull()] = 0.2

    return df


# HELPER FUNCTIONS
"""
Initialize relative scalers and encoders.
"""


def initialize_encoders(use_fitted_encoder=False):
    if use_fitted_encoder:
        scalers, ordinal_encoder = Utilities.load_encoders()
    else:
        age_scaler = sk.MinMaxScaler(AGE_SCALE)
        body_scaler = sk.MinMaxScaler(BODY_TYPE_SCALE)
        height_scaler = sk.MinMaxScaler(HEIGHT_SCALE)
        education_scaler = sk.MinMaxScaler(EDUCATION_SCALE)
        smokes_scaler = sk.MinMaxScaler(SMOKES_SCALE)

        ordinal_encoder = sk.OrdinalEncoder(
            categories=[
                BODY_TYPE_ORDINALITIES,
                EDUCATION_ORDINALITIES,
                SMOKES_ORDINALITIES,
            ],
            dtype=int,
        )

        scalers = [age_scaler, body_scaler, height_scaler, education_scaler, smokes_scaler]
    return scalers, ordinal_encoder


"""
Replace values to the predefined categories above.
"""


def consolidate_values(df):
    df = df.replace(
        {
            "body_type": {
                "athletic": "fit",
                "skinny": "thin",
                "jacked": "fit",
                "full figured": "curvy",
                "a little extra": "curvy",
                "rather not say": "average",
                "used up": "average",
                np.nan: "average",
            },
            "education": {
                "dropped out of high school": "less_than_high_school",
                "working on high school": "less_than_high_school",
                "high school": "high_school",
                "graduated from high school": "high_school",
                "dropped out of two-year college": "high_school",
                "dropped out of college/university": "high_school",
                "dropped out of law school": "completed_undergraduate_study",
                "dropped out of med school": "completed_undergraduate_study",
                "two-year college": "undergraduate_in_progress",
                "college/university": "undergraduate_in_progress",
                "working on two-year college": "undergraduate_in_progress",
                "working on college/university": "undergraduate_in_progress",
                "law school": "graduate_in_progress",
                "working on law school": "graduate_in_progress",
                "working on med school": "graduate_in_progress",
                "med school": "graduate_in_progress",
                "graduated from two-year college": "completed_undergraduate_study",
                "graduated from college/university": "completed_undergraduate_study",
                "graduated from law school": "completed_graduate_study",
                "dropped out of masters program": "completed_undergraduate_study",
                "dropped out of ph.d program": "completed_undergraduate_study",
                "masters program": "completed_undergraduate_study",
                "working on masters program": "graduate_in_progress",
                "working on ph.d program": "graduate_in_progress",
                "ph.d program": "completed_graduate_study",
                "graduated from masters program": "completed_graduate_study",
                "graduated from ph.d program": "completed_graduate_study",
                "graduated from med school": "completed_graduate_study",
                "dropped out of space camp": "high_school",
                "working on space camp": "high_school",
                "space camp": "high_school",
                "graduated from space camp": "high_school",
                np.nan: "high_school",
            },
            "smokes": {
                "when drinking": "sometimes",
                "trying to quit": "sometimes",
                np.nan: "no",
            },
            "pets": {
                "dislikes dogs and dislikes cats": "",
                "dislikes cats": "",
                "dislikes dogs": "",
                "dislikes dogs and likes cats": "cats",
                "likes cats": "cats",
                "likes dogs": "dogs",
                "likes dogs and dislikes cats": "dogs",
                "likes dogs and likes cats": "cats, dogs",
                "has cats": "cats",
                "dislikes dogs and has cats": "cats",
                "likes dogs and has cats": "cats, dogs",
                "has dogs": "dogs",
                "has dogs and dislikes cats": "dogs",
                "has dogs and likes cats": "dogs, cats",
                "has dogs and has cats": "cats, dogs",
                np.nan: "",
            },
            "religion": {
                "atheism but not too serious about it": "atheism",
                "atheism and somewhat serious about it": "atheism",
                "atheism and very serious about it": "atheism",
                "atheism and laughing about it": "atheism",
                "agnosticism but not too serious about it": "agnosticism",
                "agnosticism and somewhat serious about it": "agnosticism",
                "agnosticism and very serious about it": "agnosticism",
                "agnosticism and laughing about it": "agnosticism",
                "buddhism but not too serious about it": "buddhism",
                "buddhism and somewhat serious about it": "buddhism",
                "buddhism and very serious about it": "buddhism",
                "buddhism and laughing about it": "buddhism",
                "hinduism but not too serious about it": "hinduism",
                "hinduism and somewhat serious about it": "hinduism",
                "hinduism and very serious about it": "hinduism",
                "hinduism and laughing about it": "hinduism",
                "islam but not too serious about it": "islam",
                "islam and somewhat serious about it": "islam",
                "islam and very serious about it": "islam",
                "islam and laughing about it": "islam",
                "judaism but not too serious about it": "judaism",
                "judaism and somewhat serious about it": "judaism",
                "judaism and very serious about it": "judaism",
                "judaism and laughing about it": "judaism",
                "christianity but not too serious about it": "christianity",
                "christianity and somewhat serious about it": "christianity",
                "christianity and very serious about it": "christianity",
                "christianity and laughing about it": "christianity",
                "catholicism but not too serious about it": "catholicism",
                "catholicism and somewhat serious about it": "catholicism",
                "catholicism and very serious about it": "catholicism",
                "catholicism and laughing about it": "catholicism",
                "other but not too serious about it": "other",
                "other and somewhat serious about it": "other",
                "other and very serious about it": "other",
                "other and laughing about it": "other",
                np.nan: "unknown",
            },
        }
    )

    return df