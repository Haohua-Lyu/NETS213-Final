from matchmaker import model as Model
from matchmaker import utilities as Utilities
import pandas as pd

# The following codes are inspired by https://github.com/GlenCrawford/matchmaker.

def main():
    input = [
        [
            22,
            "a little extra",
            "graduated from two-year college",
            68.0,
            "hotel",
            "gay",
            "likes dogs and likes cats",
            "agnosticism and very serious about it",
            "m",
            "sometimes",
            "english",
            "single",
        ],
    ]
    
    compare = [
        [
            30,
            "fit",
            "working on college/university",
            75.0,
            "transportation",
            "straight",
            "likes dogs and dislikes cats",
            "judaism and laughing about it",
            "f",
            "no",
            "english",
            "single",
        ],
    ]

    input_df = pd.DataFrame(input, columns=Utilities.COLUMNS)
    neighbors = Model.execute(input_df)
    print(Utilities.sort_df(input_df), neighbors)
    compare_df = pd.DataFrame(compare, columns=Utilities.COLUMNS)
    print(Utilities.calculate_match_score(input_df, compare_df, raw=True))


if __name__ == "__main__":
    main()
