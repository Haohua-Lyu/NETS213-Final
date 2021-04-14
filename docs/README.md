# NETS213 Final Project - Documentation
#### Group members: Yueyi Wang, Aylin Özpınar, Haohua Lyu, Deniz Enfiyeci, Jasmine Jiang

### Project Overview
We use MTurk workers to create "gold standard" data about who would be good matches / bad matches. We then design a HIT where you show them the text of the dating profile of one person, and then have the workers vote on what the best match would from a set of ~5 other dating profiles.

Then we perform machine learning on the dating profile dataset by using k-nearest neighbors: Some attributes are matched using logic rules (e.g. a straight woman's candidates will be filtered down to non-gay men). Other attributes (religion, pets, children, etc) are run through a k-nearest neighbors model. This means that a certain profile and the profiles in the dataset will be plotted within an n-dimensional space along with the rest of the dating profiles, and the matches will be the ones nearest to a given profile in the space, where "nearest" effectively means similarity.

We evaluate how good our matching algorithm is by evaluating it against the MTurk “gold standard” data. We also compute the correlation coefficient between our algorithm and MTurk workers’ predictions.

### Major Components
1. Dataset Cleaning: clean datasets on OKCupid data, choose most relevant attributes - 1 pt

2. HITs creation: given one profile, ask workers to choose the best match out of 5 other profiles - 1 pt

3. Quality control: majority votes on whether a previously identified pair is a good match - 1 pt

4. Dataset splitting: split into training, validation, test sets - 1 pt

5. Model training: train a model based on KNN - 4 pt

6. Fine-tuning and evaluate ML results - 2 pt

7. Compare ML results with MTurk gold standards - 2 pt

8. Make a user interface for custom input - 2 pt

9. Write final report and prepare presentation - 2 pt

