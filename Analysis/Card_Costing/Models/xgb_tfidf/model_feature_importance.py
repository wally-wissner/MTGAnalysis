import numpy as np
import pandas as pd
from eli5 import explain_weights
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from shutil import rmtree
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from tempfile import mkdtemp
from xgboost import XGBRegressor

from Analysis.Card_Costing.report import report
from Analysis.Card_Costing.preprocessing import get_df


df = get_df()
dv = "convertedManaCost"
ivs = [col for col in df if col not in [dv, "name"]]


# NLP helper functions.
sw = set(stopwords.words("english")) - {"any", "both", "each", "you", "your"}
stemmer = SnowballStemmer(language='english')
def stem(df):
    return df.applymap(
        lambda x: (stemmer.stem(w) if all(ch.isalpha() or ch == "'" for ch in w) else w for w in x.split())
    )


pipeline_cache = mkdtemp()
pipeline = Pipeline(steps=[
    # ("stem", ColumnTransformer([("stem", FunctionTransformer(func=stem), ["text"])], remainder="passthrough")),
    ("features", FeatureUnion(transformer_list=[
        (
            "nlp",
            ColumnTransformer([
                ("tfidf", TfidfVectorizer(analyzer="word", stop_words=sw), "text"),
            ]),
        ),
        (
            "other",
            ColumnTransformer([("dropper", "drop", "text")], remainder='passthrough'),
        ),
    ])),
    ("xgb", XGBRegressor()),
], memory=pipeline_cache)
rmtree(pipeline_cache)


param_grid = {
    "features__nlp__tfidf__ngram_range": [(1, 3)],
    "features__nlp__tfidf__max_df": [2.0 ** i for i in range(-4, -1)],
    "features__nlp__tfidf__min_df": [2 ** i for i in range(4, 8)],
    "xgb__n_estimators": [50],
    "xgb__max_depth": range(4, 8),
    "xgb__learning_rate": [2 ** i for i in range(-4, 0)],
    "xgb__reg_alpha": [2 ** i for i in range(-3, 0)],
    "xgb__reg_lambda": [2 ** i for i in range(1, 6)],
}


search = report(
    df=df,
    dv=dv,
    ivs=ivs,
    pipeline=pipeline,
    param_grid=param_grid,
    rebuild_model=True,
    n_splits=3,
)
m = search.best_estimator_
