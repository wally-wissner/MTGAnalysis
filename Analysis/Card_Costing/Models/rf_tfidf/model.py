import numpy as np
import pandas as pd
from nltk.corpus import stopwords as english_stopwords
from nltk.stem.snowball import SnowballStemmer
from shutil import rmtree
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_extraction.text import TfidfVectorizer
from tempfile import mkdtemp

from Analysis.Card_Costing.report import report
from Analysis.Card_Costing.preprocessing import get_df
# from Analysis.Card_Costing.mtg_analyzer import make_mtg_analyzer, mtg_stopwords


df = get_df()
dv = "convertedManaCost"
ivs = [col for col in df if col not in [dv, "name"]]


# NLP functions.
mtg_stopwords = set(english_stopwords.words("english")) - {"any", "both", "each", "you", "your"}
_english_stemmer = SnowballStemmer(language='english')
def _analyze_string(doc, ngram_range):
    words = [
        _english_stemmer.stem(w) if all(ch.isalpha() or ch == "'" for ch in w) else w
        for w in doc.split()
        if w not in mtg_stopwords and _english_stemmer.stem(w) not in mtg_stopwords
    ]
    grams = []
    for n in (ngram_range[0], ngram_range[1] + 1):
        for word_index in range(len(words) - n):
            grams.append(" ".join(words[word_index: word_index + n - 1]))
    return grams
def mtg_analyzer(doc):
    return _analyze_string(doc, (1, 3))


pipeline_cache = mkdtemp()
pipeline = Pipeline(steps=[
    # ("stem", ColumnTransformer([("stem", FunctionTransformer(func=stem), ["text"])], remainder="passthrough")),
    ("features", FeatureUnion(transformer_list=[
        (
            "nlp",
            ColumnTransformer([
                ("tfidf", TfidfVectorizer(analyzer=mtg_analyzer, stop_words=mtg_stopwords), "text"),
                # ("svd", TruncatedSVD()),
            ]),
        ),
        (
            "other",
            ColumnTransformer([("dropper", "drop", "text")], remainder='passthrough'),
        ),
    ])),
    ("rf", RandomForestRegressor()),
], memory=pipeline_cache)


param_grid = {
    "features__nlp__tfidf__sublinear_tf": [True],
    "features__nlp__tfidf__norm": ['l2'],
    "features__nlp__tfidf__max_df": [.5],
    "features__nlp__tfidf__min_df": [20],
    # "features__nlp__svd__n_components": [50, 100, 200],
    # "best__k": [100, 500, 1000],
    "rf__max_depth": [20],
    "rf__min_samples_split": [2**i for i in range(1, 6)],
}


search = report(
    df=df,
    dv=dv,
    ivs=ivs,
    pipeline=pipeline,
    param_grid=param_grid,
    rebuild_model=False,
    n_splits=3,
)
m = search.best_estimator_
rmtree(pipeline_cache)
