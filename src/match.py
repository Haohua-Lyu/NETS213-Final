from matchmaker import model as Model
from matchmaker import utilities as Utilities
import pandas as pd

# The following codes are inspired by https://github.com/GlenCrawford/matchmaker.

def main():
    input = [
        [
            22,
            "a little extra",
            "working on college/university",
            75.0,
            "transportation",
            "gay",
            "likes dogs and likes cats",
            "agnosticism and very serious about it",
            "m",
            "sometimes",
            "english",
            "single",
        ],
    ]

    columns = [
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

    input_df = pd.DataFrame(input, columns=columns)
    neighbors = Model.execute(input_df)
    print(Utilities.sort_df(input_df), neighbors)


if __name__ == "__main__":
    main()
