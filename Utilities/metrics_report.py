import pandas as pd


def metrics_report(search):
    measures = (["mean_train", "std_train"] if search.return_train_score else []) + ["mean_test", "std_test"]
    report_cols = ["metric"] + measures
    df_metrics = pd.DataFrame(columns=report_cols)

    metrics = sorted(list({
        "_".join(col.split("_")[2:])
        for col in search.cv_results_
        if any(i in col for i in measures)
    }))

    for metric in metrics:
        row = pd.Series(
            [metric] + [search.cv_results_[f"{measure}_{metric}"][search.best_index_] for measure in measures],
            index=report_cols
        )
        df_metrics = df_metrics.append(row, ignore_index=True)

    return df_metrics
