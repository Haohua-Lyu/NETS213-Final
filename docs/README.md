# NETS213 Final Project - Documentation
#### Group members: Yueyi Wang, Aylin Özpınar, Haohua Lyu, Deniz Enfiyeci, Jasmine Jiang

### Project Overview
We use MTurk workers to create "gold standard" data about who would be good matches / bad matches. We then design a HIT where you show them the text of the dating profile of one person, and then have the workers vote on what the best match would from a set of ~5 other dating profiles.

Then we perform machine learning on the dating profile dataset by using k-nearest neighbors: Some attributes are matched using logic rules (e.g. a straight woman's candidates will be filtered down to non-gay men). Other attributes (religion, pets, children, etc) are run through a k-nearest neighbors model. This means that a certain profile and the profiles in the dataset will be plotted within an n-dimensional space along with the rest of the dating profiles, and the matches will be the ones nearest to a given profile in the space, where "nearest" effectively means similarity.

We evaluate how good our matching algorithm is by evaluating it against the MTurk “gold standard” data. We also compute the correlation coefficient between our algorithm and MTurk workers’ predictions.

### Major Components & Story Points (16pts in total)
1. Dataset Cleaning - __1 pt__
   - We will clean the datasets on OKCupid profiles, and choose the most relevant attributes appropriate and doable for our project.

2. HITs creation - __1 pt__
   - We will create our first task on MTurk: given one profile, we will ask workers to choose the best match out of 5 other profiles. This creates the gold standards needed for comparison.

3. Quality control - __1 pt__
   - We will create another task on MTurk, which serves as a higher level review of the first one; we will have majority votes on whether a previously identified pair is a good match.

4. Dataset splitting - __1 pt__
   - We will split the datasets into separate training, validation, and test sets, preparing them for machine learning models.

5. Model training - __4 pt__
   - We will perform machine learning on the dating profile dataset by using k-nearest neighbors: Some attributes are matched using logic rules (e.g. a straight woman's candidates will be filtered down to non-gay men). Other attributes (religion, pets, children, etc) are run through a k-nearest neighbors model.

6. Fine-tuning and evaluate ML results - __2 pt__
   - We will use the validation set to fine-tune our model, and then use test sets to evaluate the model's performance.

7. Compare ML results with MTurk gold standards - __2 pt__
   - We will evaluate how good our matching algorithm is by evaluating it against the MTurk “gold standard” data. We also compute the correlation coefficient between our algorithm and MTurk workers’ predictions.

8. Make a user interface for custom input - __2 pt__
   - We will make a webpage, where users can input some information and expect to see best matches returned by the ML model.

9. Write final report and prepare presentation - __2 pt__
