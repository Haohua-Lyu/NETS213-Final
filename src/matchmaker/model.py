import pandas as pd
from math import floor
from sklearn.neighbors import NearestNeighbors
from matchmaker import data_preprocessing as DataPreprocessing
from matchmaker import utilities as Utilities

# The following codes are inspired by https://github.com/GlenCrawford/matchmaker.

"""
Run the model and find k nearest neighbors.  
"""


def execute(input, k=5):
    # Original dataframe
    population_original = DataPreprocessing.load_input(False)

    # Candidates after filtering
    candidates = filter(input, population_original)
    # return if no candidates
    if len(candidates) == 0:
        return []

    # Preprocess input and population
    input_df = DataPreprocessing.preprocess_input(input.copy())
    population_df = DataPreprocessing.preprocess_input()

    # Input_df will have fewer religion columns, we need to fix it
    religion_cols = [col for col in population_df.columns if col.startswith("religion")]
    religions = pd.DataFrame([[0] * len(religion_cols)], columns=religion_cols)
    religions[input_df.iloc[:, -1].name] = input_df.iloc[:, -1]
    input_df = pd.concat([input_df.iloc[:, :-1], religions], axis=1)

    # Train the KNN model
    knn_model = NearestNeighbors(metric="braycurtis").fit(
        population_df.loc[
            :, ~population_df.columns.isin(DataPreprocessing.DIRECT_LOOKUP_FEATURES)
        ]
    )

    # Obtain neighbors
    neighbors_d, neighbors_i = knn_model.kneighbors(
        input_df.loc[
            :, ~input_df.columns.isin(DataPreprocessing.DIRECT_LOOKUP_FEATURES)
        ],
        n_neighbors=k * 20,
    )

    # Somehow the returned lists are nested...
    neighbors_d = neighbors_d[0]
    neighbors_i = neighbors_i[0]

    # Check if neighbors are in filtered candidates
    candidates_d = []
    candidates_i = []
    for i in range(len(neighbors_i)):
        if population_df.index[neighbors_i[i]] in candidates.index:
            candidates_i += [population_df.index[neighbors_i[i]]]
            candidates_d += [neighbors_d[i]]

        if len(candidates_i) >= k:
            break

    # Get neighbors's df
    neighbors_df = population_original.iloc[candidates_i].copy()
    scores = [floor((1 - d) * 100) for d in candidates_d]
    neighbors_df.insert(loc=0, column="score", value=scores)
    neighbors_df.sort_values(
        by="score", ascending=False, inplace=True, ignore_index=True
    )

    return neighbors_df


# HELPER FUNCTIONS
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
        same_sex = candidates[
            candidates["sex"] == sex
            and candidates["orientation"].isin(["gay", "bisexual"])
        ]
        opposite_sex = candidates[
            candidates["sex"] == {"m": "f", "f": "m"}[sex]
            and candidates["orientation"].isin(["straight", "bisexual"])
        ]
        candidates = pd.concat([same_sex, opposite_sex])

    return candidates