import dill as pickle
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from eli5 import explain_weights_df
from sklearn.metrics import make_scorer, mean_absolute_error, median_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV

from Utilities.metrics_report import metrics_report


def make_filtered_scorer(df, metric, filter, greater_is_better, axis=1):
    filtered = df.apply(filter, axis=axis)
    scorer = make_scorer(
        score_func=lambda y_true, y_pred: metric(
            y_true=y_true[filtered],
            y_pred=pd.Series(y_pred, index=y_true.index).loc[filtered]
        ),
        greater_is_better=greater_is_better,
    )
    return scorer


def report(df, dv, ivs, pipeline, param_grid, rebuild_model, n_jobs=1, n_splits=10, seed=0):
    search_filename = "search.pickle"
    model_filename = "model.pickle"
    report_path = "model_reports"

    def is_creature(row):
        return row["types_Creature"] == 1

    def is_noncreature(row):
        return row["types_Creature"] == 0

    scorers = {
        "neg_mae": make_scorer(mean_absolute_error, greater_is_better=False),
        "neg_mdae": make_scorer(median_absolute_error, greater_is_better=False),
        "r2": make_scorer(r2_score, greater_is_better=True),

        "neg_mae_creature": make_filtered_scorer(df, mean_absolute_error, is_creature, greater_is_better=False),
        "neg_mdae_creature": make_filtered_scorer(df, median_absolute_error, is_creature, greater_is_better=False),
        "r2_creature": make_filtered_scorer(df, r2_score, is_creature, greater_is_better=True),

        "neg_mae_noncreature": make_filtered_scorer(df, mean_absolute_error, is_noncreature, greater_is_better=False),
        "neg_mdae_noncreature": make_filtered_scorer(df, median_absolute_error, is_noncreature, greater_is_better=False),
        "r2_noncreature": make_filtered_scorer(df, r2_score, is_noncreature, greater_is_better=True),
    }

    np.random.seed(seed)

    if rebuild_model:
        search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring=scorers,
            cv=n_splits,
            refit="r2",
            return_train_score=True,
            n_jobs=n_jobs,
            verbose=10,
        )

        search.fit(X=df[ivs], y=df[dv])

        # Pickle model.
        with open(search_filename, 'wb') as f:
            pickle.dump(search, f)
        with open(model_filename, 'wb') as f:
            pickle.dump(search.best_estimator_, f)
        print("Model pickled.")


    # Load pickled model.
    with open(search_filename, 'rb') as f:
        search = pickle.load(f)
    with open(model_filename, 'rb') as f:
        m = pickle.load(f)

    if not os.path.exists(report_path):
        os.makedirs(report_path)

    with open(f"{report_path}/best_params.txt", 'w+') as f:
        f.write(str(search.best_params_))

    df_metrics = metrics_report(search)
    df_metrics.round(3).to_csv(f"{report_path}/metrics.csv", index=False)

    explain_weights_df(m).round(3).to_csv(f"{report_path}/eli5_explanation.csv", index=False)

    return search
