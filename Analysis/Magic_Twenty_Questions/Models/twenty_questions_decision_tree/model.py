from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier


m = Pipeline(steps=[
    DecisionTreeClassifier(),
])


