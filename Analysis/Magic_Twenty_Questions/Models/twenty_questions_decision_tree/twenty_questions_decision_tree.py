from sklearn.base import BaseEstimator, ClassifierMixin


class TreeNode(object):
    def __init__(self, feature, condition):
        self.feature = feature
        self.condition = condition



class TwentyQuestionsDecisionTree(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.dtypes = None
        self.current_node = None

    def fit(self, X, y):
        self.dtypes = X.dtypes

    def predict(self, X):


    def ask(self):
