from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import InlineRadios


class ProfileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "form"
        self.helper.form_method = "post"
        self.helper.form_action = "matches"

        self.helper.layout = Layout(
            Fieldset(
                "About you:",
                InlineRadios("sex"),
                InlineRadios("orientation"),
                "age",
                "speaks",
                "body_type",
                "height",
                "education",
                "job",
                "religion",
                "smokes",
                "pets",
            ),
            ButtonHolder(Submit("submit", "Submit")),
        )

    # Fields.
    sex = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Sex",
        required=True,
        choices=[("m", "Male"), ("f", "Female")],
    )
    orientation = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Sexual orientation",
        required=True,
        choices=[("straight", "Straight"), ("gay", "Gay"), ("bisexual", "Bisexual")],
        initial="",
    )
    age = forms.IntegerField(label="Age", required=True, min_value=18, max_value=110)
    job = forms.CharField(label="Job", required=True, max_length=80)
    speaks = forms.ChoiceField(
        label="Language",
        required=True,
        choices=[
            ("", ""),
            ("afrikaans", "Afrikaans"),
            ("english", "English"),
            ("french", "French"),
            ("hindi", "Hindi"),
            ("japanese", "Japanese"),
            ("mandarin_chinese", "Mandarin Chinese"),
            ("portuguese", "Portuguese"),
            ("russian", "Russian"),
            ("spanish", "Spanish"),
        ],
        initial="",
    )
    religion = forms.ChoiceField(
        label="Religion",
        required=True,
        choices=[
            ("", ""),
            ("atheism", "Atheism"),
            ("agnosticism", "Agnosticism"),
            ("buddhism", "Buddhism"),
            ("hinduism", "Hinduism"),
            ("islam", "Islam"),
            ("judaism", "Judaism"),
            ("christianity", "Christianity"),
            ("catholicism", "Catholicism"),
            ("other", "Other"),
        ],
        initial="",
    )
    education = forms.ChoiceField(
        label="Education level",
        required=True,
        choices=[
            ("", ""),
            ("less_than_high_school", "Less than high school"),
            ("high_school", "High school"),
            ("undergraduate_in_progress", "Undergraduate (in progress)"),
            ("completed_undergraduate_study", "Undergraduate completed"),
            ("graduate_in_progress", "Graduate (in progress)"),
            ("completed_graduate_study", "Graduate completed"),
        ],
        initial="",
    )
    body_type = forms.ChoiceField(
        label="Body type",
        required=True,
        choices=[
            ("", ""),
            ("thin", "Thin"),
            ("fit", "Fit"),
            ("average", "Average"),
            ("curvy", "Curvy"),
            ("overweight", "Overweight"),
        ],
        initial="",
    )
    height = forms.IntegerField(
        label="Height (in inches)", required=True, min_value=0, max_value=150
    )
    smokes = forms.ChoiceField(
        label="Smokes?",
        required=True,
        choices=[("", ""), ("no", "No"), ("yes", "Yes"), ("sometimes", "Sometimes")],
        initial="",
    )
    pets = forms.ChoiceField(
        label="Pets",
        required=False,
        choices=[
            ("", ""),
            ("", "None"),
            ("cats", "Like/have cat(s)"),
            ("dogs", "Like/have dog(s)"),
            ("cats, dogs", "Like/have cat(s) and dog(s)"),
        ],
        initial="",
    )
