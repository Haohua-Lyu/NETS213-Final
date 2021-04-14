# NETS213 Final Project - Overview
#### Group members: Yueyi Wang, Aylin Özpınar, Haohua Lyu, Deniz Enfiyeci, Jasmine Jiang

### Project Overview
We use MTurk workers to create "gold standard" data about who would be good matches / bad matches. We then design a HIT where you show them the text of the dating profile of one person, and then have the workers vote on what the best match would from a set of ~5 other dating profiles.

Then we perform machine learning on the dating profile dataset by using k-nearest neighbors: Some attributes are matched using logic rules (e.g. a straight woman's candidates will be filtered down to non-gay men). Other attributes (religion, pets, children, etc) are run through a k-nearest neighbors model. This means that a certain profile and the profiles in the dataset will be plotted within an n-dimensional space along with the rest of the dating profiles, and the matches will be the ones nearest to a given profile in the space, where "nearest" effectively means similarity.

We evaluate how good our matching algorithm is by evaluating it against the MTurk “gold standard” data. We also compute the correlation coefficient between our algorithm and MTurk workers’ predictions.

### Files
- In the ```docs/``` directory:
  - ```flow_diagram.png``` is the flow diagram for our project design.
  - ```HIT_mockup.png``` is the mockup of our first task, where we would show one profile and ask workers to choose a best match from a set of ~5 profiles. The interface of the second task would be very similar; two profiles will be shown and workers only need to indicate whether they think it is a good match.
  - ```User_interface_mockup``` is the mockup of our final user interface. It will be a webpage, where users can input some information and expect to see best matches returned by the ML model.
  - ```README.md``` includes the major components and story points.
- In the ```data/``` directory: *(Deliverable 2)*
- In the ```src/``` directory: *(Deliverable 2)*
