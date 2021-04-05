import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from shutil import rmtree
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from tempfile import mkdtemp
from xgboost import XGBRegressor

from Analysis.Card_Costing.report import report
from Analysis.Card_Costing.preprocessing import get_df


df = get_df()
dv = "convertedManaCost"
ivs = [col for col in df if col not in [dv, "name"]]


# NLP helper functions.
analyzer = CountVectorizer().build_analyzer()
sw = set(stopwords.words("english")) - {"any", "both", "each", "you", "your"}
stemmer = SnowballStemmer(language='english')
def stemming(doc):
    # Only stem English words.
    return (stemmer.stem(w) if all(ch.isalpha() or ch == "'" for ch in w) else w for w in analyzer(doc))


pipeline_cache = mkdtemp()
nlp_pipeline = Pipeline(steps=[
    ("vect", ColumnTransformer([
        ("tfidf", TfidfVectorizer(
            analyzer="word",
            stop_words=sw,
        ), "text")
    ])),
    # ("svd", TruncatedSVD()),
    # ("best", SelectKBest()),
])
other_pipeline = Pipeline(steps=[
    ("drop_nlp", ColumnTransformer([("dropper", "drop", "text")], remainder='passthrough')),
])
pipeline = Pipeline(
    steps=[
        (
            "features",
            FeatureUnion(
                transformer_list=[
                    ("nlp", nlp_pipeline),
                    ("other", other_pipeline),
                ]
            )
        ),
        ("xgb", XGBRegressor(booster="gbtree", n_jobs=4)),
    ],
    memory=pipeline_cache,
)
rmtree(pipeline_cache)


param_grid = {
    "features__nlp__vect__tfidf__ngram_range": [(1, 3)],
    "features__nlp__vect__tfidf__max_df": [2 ** i for i in range(-4, 0)],
    "features__nlp__vect__tfidf__min_df": [2 ** i for i in range(4, 8)],
    # "features__nlp__vect__tfidf__max_features": [5000],
    # "features__nlp__best__k": [5000],
    # "features__nlp__svd__n_components": [100],
    "xgb__n_estimators": [50],
    "xgb__max_depth": [20],
    "xgb__learning_rate": [2 ** i for i in range(-4, 0)],
    "xgb__reg_alpha": [2 ** i for i in range(-3, 0)],
    "xgb__reg_lambda": [2 ** i for i in range(0, 3)],
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
