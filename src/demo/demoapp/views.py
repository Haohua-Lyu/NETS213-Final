from django.shortcuts import render
from .forms import ProfileForm
import sys

sys.path.append(r"D:\Penn\Y4S2\NETS 213\Final\NETS213-Final\src")
from datehive import utilities as Utilities
from datehive import model as Model
import pandas as pd
import numpy as np

# Create your views here.
def index(request):
    context = {"form": ProfileForm()}
    return render(request, "home.html", context)


def matches(request):
    form = ProfileForm(request.POST)

    if form.is_valid():
        input = [
            [
                form.cleaned_data["age"],
                form.cleaned_data["body_type"],
                form.cleaned_data["education"],
                form.cleaned_data["height"],
                form.cleaned_data["job"],
                form.cleaned_data["orientation"],
                form.cleaned_data["pets"],
                form.cleaned_data["religion"],
                form.cleaned_data["sex"],
                form.cleaned_data["smokes"],
                form.cleaned_data["speaks"],
                "single",
            ]
        ]

        input_df = pd.DataFrame(input, columns=Utilities.COLUMNS)

        matches_df = Model.execute(input_df)

    matches = []

    for _, row in matches_df.iterrows():
        match = [
            row["age"],
            row["score"],
            row["body_type"],
            row["education"],
            row["height"],
            row["job"],
            row["orientation"],
            row["pets"],
            row["religion"],
            'Female' if row["sex"] == 'f' else 'Male',
            row["smokes"],
            row["speaks"],
            row["status"],
        ]
        match = ['Unknown' if str(val) == 'nan' else val for val in match]
        matches += [match]

    context = {"matches": matches}

    return render(request, "matches.html", context)
