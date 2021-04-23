# NETS213 Final Project - Overview
#### Group members: Yueyi Wang, Aylin Özpınar, Haohua Lyu, Deniz Enfiyeci, Jasmine Jiang

### Project Overview
We use MTurk workers to create "gold standard" data about who would be good matches / bad matches. We then design a HIT where you show them the text of the dating profile of one person, and then have the workers vote on what the best match would from a set of ~5 other dating profiles.

Then we perform machine learning on the dating profile dataset by using k-nearest neighbors: Some attributes are matched using logic rules (e.g. a straight woman's candidates will be filtered down to non-gay men). Other attributes (religion, pets, children, etc) are run through a k-nearest neighbors model. This means that a certain profile and the profiles in the dataset will be plotted within an n-dimensional space along with the rest of the dating profiles, and the matches will be the ones nearest to a given profile in the space, where "nearest" effectively means similarity.

We evaluate how good our matching algorithm is by evaluating it against the MTurk “gold standard” data. We also compute the correlation coefficient between our algorithm and MTurk workers’ predictions.

### Files
- In the ```docs/``` directory:
  - ```flow_diagram.png``` is the flow diagram for our project design.
  - ```HIT_mockup.png``` is the mockup of our MTurk task, where we would show one profile and ask workers to choose a best match from a set of ~5 profiles.
  - ```User_interface_mockup.png``` is the mockup of our final user interface. It will be a webpage, where users can input some information and expect to see best matches returned by the ML model.
  - ```README.md``` includes the major components and story points.
- In the ```data/``` directory: 
  - ```okcupid_clean.csv``` is the raw data of our project. It contains cleaned profiles of some OkCupid users, and we will use them to train classifiers and create gold standards.
  - ```SAMPLE-INPUT-FOR-AGGREGATION.csv```, ```SAMPLE-OUTPUT-FOR-AGGREGATION.csv``` are the sample inputs/outputs of the aggregation module (```src/aggregation_module.py```).
  - ```SAMPLE-INPUT-FOR-QC.csv```, ```SAMPLE-OUTPUT-FOR-QC.csv``` are the sample inputs/outputs of the quality control module (```src/QC-Module.py```).
- In the ```src/``` directory: 
  - ```aggregation_module.py``` is the Python file for the aggregation module.
  - ```QC-Module.py``` is the Python file for the quality control module.

### Major Components & Story Points (17pts in total)
1. Dataset Cleaning - __1 pt__
   - We will clean the datasets on OKCupid profiles, and choose the most relevant attributes appropriate and doable for our project.

2. HITs creation - __1 pt__
   - We will create our first task on MTurk: given one profile, we will ask workers to choose the best match out of 5 other profiles. This creates the gold standards needed for comparison.

3. Aggregation - __1 pt__
   - We will download the results from MTurk and aggregate the matched pairs that are selected by workers through collections (weighted by numbers of selection).

4. Quality control - __1 pt__
   - We will run the EM algorithm on the aggregated pairs to decide whether a previously identified pair is a good match.

5. Dataset splitting - __1 pt__
   - We will split the datasets into separate training, validation, and test sets, preparing them for machine learning models.

6. Model training - __4 pt__
   - We will perform machine learning on the dating profile dataset by using k-nearest neighbors: Some attributes are matched using logic rules (e.g. a straight woman's candidates will be filtered down to non-gay men). Other attributes (religion, pets, children, etc) are run through a k-nearest neighbors model.

7. Fine-tuning and evaluate ML results - __2 pt__
   - We will use the validation set to fine-tune our model, and then use test sets to evaluate the model's performance.

8. Compare ML results with MTurk gold standards - __2 pt__
   - We will evaluate how good our matching algorithm is by evaluating it against the MTurk “gold standard” data. We also compute the correlation coefficient between our algorithm and MTurk workers’ predictions.

9.  Make a user interface for custom input - __2 pt__
    - We will make a webpage, where users can input some information and expect to see best matches returned by the ML model.

10. Write final report and prepare presentation - __2 pt__

### Data
- The raw data we are using is called ```okcupid_clean.csv```. Currently, it includes 12 columns and 59939 rows. Each row corresponds to a profile and each cell contains a different answer to 12 questions specified in the columns. Prior to cleaning, the data included duplicates, varying status answers, and 8 more columns. We started by removing the duplicates and standardizing the varying status answers to single, seeing someone, married, or NaN. The 8 columns dropped were diet, drugs, sign, ethnicity, income, offspring, and drinks. We did not want to use there metrics in our matching algorithm and found them irrelevant. 
- Our aggregation takes place before the quality control module, so the sample output for aggregation is identical to the sample input of the QC module. Aggregation module takes in worker results from MTurk and turns them to profile pairs with individual grading; QC module takes those pairs and produce labels. 

### Aggregation & Quality Control Codes
- In the aggregation module, we simply collect all the possible profile pairs from each row in the dataset, and output all the profile pairs and the corresponding ratings for each pair
- In the Quality Control module, we use the EM Algorithm to perform quality control. We first assume the workers have perfect qualities, and use this assumption to compute the "correct" labels for each profile pairs to see if there is a match or not. We then use the labels to calculate the worker qualities and corresponding ratings, and finally determine if the current pair should be a match or not.
